from bot.helper import dp
from aiogram import executor
from bot.handlers.user import register_user
from database.main_db import db_start


async def on_startup(_):
    print('Bot went online!')
    await db_start()

register_user(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
