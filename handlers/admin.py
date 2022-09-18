from aiogram.types import Message
from aiogram.dispatcher import Dispatcher


async def backup(msg: Message):
    await msg.answer_document(open('data/user_data.db', 'br'),
                              caption=f"This is your backup for {msg.date.date()}")


def register_admin(dp: Dispatcher):
    dp.register_message_handler(backup,
                                lambda msg: msg.from_user.id == 126073578,
                                commands='backup')
