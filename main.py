import logging
from helper import dp
from aiogram import executor
from handlers.user import register_user
from database.main_db import db_start
from handlers.user_commands import register_user_commands
from handlers.user_search import register_search
from handlers.admin import register_admin

WEBHOOK_HOST = 'https://ritsu.uwussi.moe'
WEBHOOK_PATH = '/'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = '127.0.0.1'
WEBAPP_PORT = 7771


async def on_startup(bot):
    await bot.set_webhook(WEBHOOK_URL)
    await db_start()


async def on_shutdown(bot):
    await bot.delete_webhook()


register_user(dp)
register_user_commands(dp)
register_admin(dp)
register_search(dp)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    executor.start_webhook(
        dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT
    )
