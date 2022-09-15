from bot.helper import dp
from aiogram import executor
from bot.handlers.user import register_user


async def on_startup(_):
    print('Bot went online!')

register_user(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
