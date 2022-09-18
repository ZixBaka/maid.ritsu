import os
import logging
from helper import dp
from aiogram import executor
from handlers.user import register_user
from database.main_db import db_start
from handlers.user_commands import register_user_commands
from handlers.user_search import register_search
from handlers.admin import register_admin


async def on_startup(_):
    print('Bot went online!')
    await db_start()

register_user(dp)
register_user_commands(dp)
register_admin(dp)
register_search(dp)


if __name__ == '__main__':
    if not os.path.exists('data'):
        os.mkdir('data')

    logging.basicConfig(level=logging.DEBUG)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
