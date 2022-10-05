import asyncio

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.exceptions import BotBlocked

from tgbot.keyboards.admin_kb import admin_menu, admin_cars_keyboard, admin_menu_call_data, admin_cars_call_data, \
    admin_drivers_keyboard, admin_driver_call_data
from tgbot.keyboards.inline import feedback_keyboard
from tgbot.misc.states import AdminStates
from tgbot.models.cars import Car
from tgbot.models.students import Student
from tgbot.misc.states import Menu


async def admin_start(message: Message):
    await message.reply("Hello, admin!", reply_markup=admin_menu)
    await AdminStates.in_admin_panel.set()


async def send_chat(call: CallbackQuery):
    await call.message.answer("telegram id is needed")
    await AdminStates.selecting_partner_for_chatting.set()


async def select_chat_partner(msg: Message):

    partner = Student.get_student(msg.bot.get("db"), tg_id=int(msg.text))
    if partner is None:
        await msg.answer("This user has ")


async def admin_cars(call: CallbackQuery):
    await call.message.delete()
    await call.message.answer("Send me a number")
    await AdminStates.search_car.set()


async def admin_find_car_number(msg: Message, state: FSMContext):
    session_maker = msg.bot.get("db")
    cars = await Car.get_cars(session_maker=session_maker, car_number=msg.text)
    if len(cars) == 0:
        await msg.answer("Looks like car with this number doesn't exist")
    else:
        for c in cars:
            status = "enabled"
            if c.status == 0:
                status = "disabled"
            await msg.answer(f'Order: {c.car_order}\n\n'
                             f'Car number: <code>{c.car_number}</code>\n\n'
                             f'Car owner id: <code>{c.owner}</code>\n\n'
                             f'Car status: <code>{status}</code>',
                             reply_markup=admin_cars_keyboard(c.car_order, c.owner))
            await asyncio.sleep(0.3)
    await state.finish()


async def disable_car(call: CallbackQuery, callback_data: dict, state: FSMContext):

    await Car.update_status_by_order(session_maker=call.bot.get("db"),
                                     order=int(callback_data.get("order")),
                                     status=dict(status=0))
    await call.answer("This car is disabled!")
    await call.message.delete()
    await state.finish()


async def enable_car(call: CallbackQuery, callback_data: dict, state: FSMContext):

    await Car.update_status_by_order(session_maker=call.bot.get("db"),
                                     order=int(callback_data.get("order")),
                                     status=dict(status=1))

    await call.answer("This car is enabled!")
    await call.message.delete()
    await state.finish()


async def admin_drivers(call: CallbackQuery):
    await call.message.delete()
    await call.message.answer("Ok, send me a driver telegram_id")
    await AdminStates.search_driver.set()


async def admin_find_driver(msg: Message, state: FSMContext):
    try:
        student = await Student.get_any_student(session_maker=msg.bot.get("db"), tg_id=int(msg.text))
        if student is None:
            await msg.answer("Student with this id doesn't exist in our database")
        else:
            cars = await Car.get_all_by_tg(session_maker=msg.bot.get("db"), tg_id=student.tg_id)

            status = "active"
            if student.status == 0:
                status = "banned"

            car_nums = "\n\n"
            for c in cars:
                car_nums += "<code>" + str(c.car_order) + " " + c.car_number + "\n\n</code>"
            await msg.answer(f'Student id: <code>{student.tg_id}</code>\n\n'
                             f'Student first name: <code>{student.first_name}</code>\n\n'
                             f'Student phone number: <code>{student.phone_number}</code>\n\n'
                             f'Student status: <code>{status}</code>\n\n'
                             f'Cars: {car_nums}',
                             reply_markup=admin_drivers_keyboard(student.tg_id, student.tg_id))
            await state.finish()
    except ValueError:
        await msg.answer("It's not an ID bruh")


async def ban_driver(call: CallbackQuery, callback_data: dict, state: FSMContext):
    student = Student(tg_id=int(callback_data.get("driver")))
    await student.update_client(session_maker=call.bot.get("db"),
                                updated_fields=dict(status=0))
    await call.answer("This car is disabled!")
    await call.message.delete()
    await state.finish()


async def unban_driver(call: CallbackQuery, callback_data: dict, state: FSMContext):
    student = Student(tg_id=int(callback_data.get("driver")))
    await student.update_client(session_maker=call.bot.get("db"),
                                updated_fields=dict(status=1))
    await call.answer("This car is disabled!")
    await call.message.delete()
    await state.finish()


async def hide(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    if state != "":
        await state.finish()


# ================ADMIN CHAT===================
async def chat(call: CallbackQuery, callback_data: dict,  state: FSMContext):
    driver_id = callback_data.get("driver")

    start_text = f"🟢<b>The dialogue has begun</b>💬\n" \
                 f"<i>You can write messages and they will be\nsent to the owner of the car</i>"

    start_text_r = f"🟢<b>ADMIN started dialogue with you</b>💬\n" \
                   f"<b>All your messages will be redirected to admin from now</b>"
    # who called
    try:
        await call.message.edit_text(start_text)
        await call.message.edit_reply_markup(feedback_keyboard)

        await call.message.bot.send_message(driver_id, start_text_r, reply_markup=feedback_keyboard)

        await state.storage.set_state(chat=driver_id, user=driver_id, state=Menu.in_discussion_with_admin.state)

        await AdminStates.in_discussion_with_reporter.set()

        await state.update_data(dict(reporter=driver_id))

    except BotBlocked:
        await call.message.answer('Bot was blocked by the user :/')
        await state.finish()


async def discussion_with_reporter(msg: Message, state: FSMContext):
    data = await state.get_data()
    reporter = data.get("reporter")
    try:
        await msg.bot.send_message(
            int(reporter),
            f"<b>Admin</b>"
            f"\n\n<i>{msg.text}</i>"
            f"\n\n\n /finish to finish the conversation")

    except BotBlocked:
        await msg.reply("The bot blocked by user")
        await state.finish()


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, state=["*", ""], commands=["admin"], is_admin=True)
    # =======Chat======
    dp.register_callback_query_handler(chat, admin_driver_call_data.filter(
        action=['start_discussion', "start_chat"]))

    dp.register_message_handler(discussion_with_reporter, commands="finish",
                                state=AdminStates.in_discussion_with_reporter)

    dp.register_message_handler(discussion_with_reporter, state=AdminStates.in_discussion_with_reporter)
    dp.register_callback_query_handler(hide, admin_menu_call_data.filter(action="hide"))
    # =======Cars======
    dp.register_callback_query_handler(admin_cars, admin_menu_call_data.filter(action="find_car"),
                                       state=AdminStates.in_admin_panel, is_admin=True)
    dp.register_message_handler(admin_find_car_number, state=AdminStates.search_car, is_admin=True)
    dp.register_callback_query_handler(disable_car, admin_cars_call_data.filter(action="disable"), state=["*", ""],
                                       is_admin=True)
    dp.register_callback_query_handler(enable_car, admin_cars_call_data.filter(action="enable"), state=["*", ""],
                                       is_admin=True)

    # ======Drivers======
    dp.register_callback_query_handler(admin_drivers,  admin_menu_call_data.filter(action="find_driver"),
                                       state=AdminStates.in_admin_panel, is_admin=True)
    dp.register_message_handler(admin_find_driver, state=AdminStates.search_driver, is_admin=True)
    dp.register_callback_query_handler(ban_driver, admin_driver_call_data.filter(action="ban_driver"),
                                       state=["*", ""], is_admin=True)
    dp.register_callback_query_handler(unban_driver, admin_driver_call_data.filter(action="unban_driver"),
                                       state=["*", ""], is_admin=True)
    # ========Universal button=======
    dp.register_callback_query_handler(hide, admin_menu_call_data.filter(action="hide"), state=["*", ""],
                                       is_admin=True)
