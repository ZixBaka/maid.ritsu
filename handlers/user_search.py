from aiogram.types import Message, CallbackQuery, ParseMode
from aiogram.dispatcher import Dispatcher
from bot.filters.valid_number import is_valid
from asyncio import gather
from bot.database.main_db import search_db, de_check_user_db
from bot.keyboards.user_register_inline import notify_kb
from bot.helper import bot
from aiogram.utils.exceptions import BotBlocked


async def search(msg: Message):
    await (respond := gather(search_db(msg.text.upper())))
    try:
        await notify_kb(msg, respond.result()[0])
    except TypeError:
        await msg.answer('🙅‍♂️Nothing was found 😕')


async def error_1(msg: Message):
    await msg.answer('⚠You are not registered!\n Use /register')


async def notify(callback: CallbackQuery):
    await callback.message.delete()
    notify_text = f"👋Hello!\n" \
                  f"❗YOUR CAR <b>PREVENTS</b> ANOTHER CAR\n" \
                  f"❕FROM LEAVING THE PARKING LOT\n" \
                  f"\n" \
                  f"🙏Please come to your car\n" \
                  f"👤Request from: <a href='https://t.me/{callback.from_user.username}'>" \
                  f"{callback.from_user.first_name}</a>"
    try:
        await bot.send_message(callback.data, notify_text,
                               parse_mode=ParseMode.HTML,
                               disable_web_page_preview=True)
    except BotBlocked:
        await callback.message.answer("The owner of the car deleted/blocked the bot😐")


def register_search(dp: Dispatcher):
    dp.register_message_handler(search,
                                lambda msg: is_valid(msg.text) and de_check_user_db(msg.from_user.id))
    dp.register_message_handler(error_1, lambda msg: is_valid(msg.text))
    # notify handle
    dp.register_callback_query_handler(notify)
