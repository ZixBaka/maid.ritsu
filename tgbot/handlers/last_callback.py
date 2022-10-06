from aiogram.types import CallbackQuery
from aiogram import Dispatcher


async def lost(call: CallbackQuery):
    await call.answer('Time out')


<<<<<<< HEAD
def register_unhandled_call(dp: Dispatcher):
    dp.register_callback_query_handler(lost, state='*')
=======
async def error_late_finish(call: CallbackQuery):
    await call.answer('🟡The chat has already finished or you restarted the bot')


def register_unhandled_call(dp: Dispatcher):
    dp.register_callback_query_handler(lost, state='*')
    dp.register_callback_query_handler(error_late_finish, text="back_to_menu")
>>>>>>> pr/11
