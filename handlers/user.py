from aiogram.dispatcher import Dispatcher
from aiogram.types import Message


async def echo(msg: Message):
    await msg.answer(msg.text)


def register_user(dp: Dispatcher):
    dp.register_message_handler(echo)