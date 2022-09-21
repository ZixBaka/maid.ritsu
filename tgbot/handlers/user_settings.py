from aiogram import Dispatcher, types
from aiogram.types import Message, InlineQuery, InlineQueryResultArticle, InputTextMessageContent, CallbackQuery
from sqlalchemy.orm import sessionmaker

from tgbot.keyboards.inline import main_car_inline_keyboard, separate_car_inline_keyboard, car_callback, \
    main_menu_keyboard, settings_keyboard
from tgbot.misc.states import Menu
from tgbot.models.cars import Car


async def check_cars(query: InlineQuery):
    cars = await Car.get_all_by_tg(query.bot.get("db"), query.from_user.id)
    car_numbers = []
    for car in cars:
        car_numbers.append(InlineQueryResultArticle(
            id=f"{car.car_number}",
            title=f"{car.car_number}",
            reply_markup=separate_car_inline_keyboard(car.car_number),
            input_message_content=InputTextMessageContent(
                message_text=f"<b>{car.car_number}</b>",
            )))

    await query.answer(
        results=car_numbers,
        cache_time=2)


async def cars_settings(msg: Message):
    await msg.answer("<b>Okay, what do you want to do with your cars?!</b>",
                     reply_markup=main_car_inline_keyboard)
    await Menu.car_settings.set()


async def add_car(call: CallbackQuery):
    await call.message.delete()
    await call.message.answer("<b>Send me your car number pweese...</b>")
    await Menu.add_car.set()


async def insert_card_number(msg: Message):
    session_maker: sessionmaker = msg.bot.get("db")
    car_num = msg.text.upper().replace(" ", "")
    await msg.reply("\n".join([
        "<b>WoW, there is one more car in yor list</b>"
    ]), reply_markup=settings_keyboard)

    await Car.add_car(session_maker, car_number=car_num, owner=msg.from_user.id)
    await Menu.settings.set()


async def car_number_exist(msg: Message, ):
    await msg.answer(
        "<b>Looks like your car number is already taken, please contact admin via /report if necessary</b>",
        reply_markup=main_menu_keyboard)

    await Menu.in_main_menu.set()


async def close_car_msg(call: CallbackQuery):
    await call.message.delete()
    await Menu.settings.set()


async def delete_the_car(call: CallbackQuery, callback_data: dict):
    car_number = callback_data.get("number")
    await call.answer()

    if await Car.get_car(call.bot.get("db"), car_number) is None:
        await call.bot.send_message(call.from_user.id, "<b>You don't own this car 0_o</b>",
                                    reply_markup=main_menu_keyboard)
    else:
        await call.bot.send_message(call.from_user.id, "<b>I successfully deleted the car ^^</b>",
                                    reply_markup=main_menu_keyboard)
        await Car.delete_car(call.bot.get("db"), car_number)
    await Menu.in_main_menu.set()


async def edit_the_car(call: CallbackQuery, callback_data: dict):
    car_number = callback_data.get("number")
    await call.answer()

    car_to_be_edited = await Car.get_car(call.bot.get("db"), car_number)
    if car_to_be_edited is None:
        await call.bot.send_message(call.from_user.id, "<b>You don't own this car 0_o</b>")
    else:
        await call.bot.send_message(call.from_user.id, "<b>I successfully deleted the car ^^</b>")
        await Car.delete_car(call.bot.get("db"), car_number)
    await Menu.edit_car()


async def update_card_number(msg: Message):
    session_maker: sessionmaker = msg.bot.get("db")
    car_num = msg.text.upper().replace(" ", "")
    await msg.reply("\n".join([
        "<b>We updated your car info</b>"
    ]), reply_markup=settings_keyboard)

    await Car.add_car(session_maker, car_number=car_num, owner=msg.from_user.id)
    await Menu.settings.set()


def user_settings_handlers(dp: Dispatcher):
    dp.register_inline_handler(check_cars, state=Menu.car_settings)
    dp.register_callback_query_handler(cars_settings, text="Cars", state=Menu.settings, in_db=True)
    dp.register_callback_query_handler(close_car_msg, state=Menu.car_settings, text="close_car")
    dp.register_callback_query_handler(add_car,  text="add_car", state=Menu.car_settings)
    dp.register_message_handler(insert_card_number,  content_types=types.ContentType.TEXT, state=Menu.add_car,
                                car_in_db=False)
    dp.register_message_handler(car_number_exist,  content_types=types.ContentType.TEXT, state=Menu.add_car,
                                car_in_db=True)
    dp.register_callback_query_handler(delete_the_car, car_callback.filter(method="delete"), state=Menu.car_settings)

