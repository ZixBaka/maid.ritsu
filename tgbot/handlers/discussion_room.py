from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, InlineQueryResultArticle, InlineQuery, InputTextMessageContent, CallbackQuery

from tgbot.config import Config
from tgbot.keyboards.inline import found_driver_keyboard
from tgbot.misc.states import Menu
from tgbot.models.cars import Car


async def feedback_discussion(msg: Message):
    config: Config = msg.bot.get("config")

    await msg.bot.send_message(
        config.tg_bot.admins_group[0],
        "".join([f"<b>From user:\n <a href='tg://user?id={msg.from_user.id}'>{msg.from_user.first_name}</a></b>\n\n",
                 f"<i>{msg.text}</i>"],
                ))


async def search_owner(query: InlineQuery, cars: [Car]):
    car_numbers = []
    print(cars)
    for car in cars:
        car_numbers.append(InlineQueryResultArticle(
            id=f"{car.car_number}",
            title=f"{car.car_number}",
            reply_markup=found_driver_keyboard(car.car_number),
            input_message_content=InputTextMessageContent(
                message_text=f"<b>{car.car_number}</b>",
            )))
    await query.answer(
        results=car_numbers,
        cache_time=2)


async def cancel_searching(call: CallbackQuery):
    await call.message.delete()
    await Menu.in_main_menu.set()


async def cancel_chatting(call: CallbackQuery):
    await call.answer()
    await Menu.in_main_menu.set()


async def start_chatting(call: CallbackQuery, callback_data: dict, state: FSMContext):
    car_number = callback_data.get("number")
    await call.bot.send_message(call.from_user.id,
                                "<b>You can write now, all messages will be delivered to the car owner.</b>\n write /finish to end a chat",
                                )
    car_owner = await Car.get_car(call.bot.get("db"), car_number)

    await state.update_data(dict(partner=car_owner.owner))


# async def enter_discussion(call: CallbackQuery, callback_data: dict):
#     car_number =
#
# async def send_message(msg: Message, state: ):


def discussion_handlers(dp: Dispatcher):
    dp.register_message_handler(feedback_discussion, state=Menu.feedback)
    dp.register_inline_handler(search_owner, search_car=True, state=Menu.search_student)
    dp.register_callback_query_handler(cancel_searching, text="cancel_searching", state=Menu.search_student)
    dp.register_callback_query_handler(cancel_chatting, text="cancel_chatting", state=Menu.search_student)


