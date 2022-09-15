from bot.helper import dp
from aiogram import executor


async def on_startup(_):
    print('Bot went online!')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
