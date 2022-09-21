from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery

from tgbot.keyboards.inline import settings_keyboard, feedback_keyboard, about_us_keyboard, main_menu_keyboard
from tgbot.misc.states import Menu


async def settings(call: CallbackQuery):
    await call.message.delete()
    await call.message.answer(
        "".join(["<b> In this section, you can manage</b>"
                 "<b> information that related to you.</b>"]),
        reply_markup=settings_keyboard)

    await Menu.settings.set()

async def feedback(call: CallbackQuery):
    await call.message.delete()

    # TODO: answer text
    await call.message.answer("".join(["<b>Now, everything you write here will be forwarded ",
                                       "to admins. Then, they can contact you directly or via me if needed</b>",
                                       "<i>send /finish to end feedback massage</i>"]),
                              reply_markup=feedback_keyboard
                              )
    await Menu.feedback.set()


async def about_us(call: CallbackQuery):
    await call.message.delete()
    # TODO: answer text
    await call.message.answer("<b> We are bla bla bla...</b>", reply_markup=about_us_keyboard)

    await Menu.about_us.set()


async def exit_to_menu(call: CallbackQuery):
    # TODO: answer text

    await call.message.answer(text="#<code>main menu text</code>", reply_markup=main_menu_keyboard)
    await call.message.delete()

    await Menu.in_main_menu.set()


async def finish(msg: Message):

    await msg.answer(text="#<code>main menu text</code>", reply_markup=main_menu_keyboard)
    await msg.delete()

    await Menu.in_main_menu.set()


def user_menu_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(settings, text="settings", state=Menu.in_main_menu, in_db=True)
    dp.register_callback_query_handler(about_us, text="about", state=Menu.in_main_menu, in_db=True)

    dp.register_message_handler(finish, commands="finish", state=Menu.feedback)
    dp.register_callback_query_handler(feedback, text="feedback", state=Menu.in_main_menu, in_db=True)

    dp.register_callback_query_handler(exit_to_menu, text="back_to_menu", state="*")

