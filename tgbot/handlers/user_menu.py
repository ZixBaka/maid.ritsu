from aiogram import Dispatcher
from aiogram.types import Message, InlineQuery, InlineQueryResultArticle, InputTextMessageContent

from tgbot.keyboards.inline import main_car_inline_keyboard, separate_car_inline_keyboard, search_driver_keyboard
from tgbot.keyboards.reply import settings_keyboard, feedback_keyboard, main_menu_keyboard, about_us_keyboard
from tgbot.misc.states import Menu
from tgbot.models.cars import Car


async def settings(msg: Message):
    await msg.answer("".join(["<b> In this section, you can manage</b>"
                              "<b> information that related to you.</b>"]),
                     reply_markup=settings_keyboard)

    await Menu.settings.set()


async def feedback(msg: Message):
    await msg.answer("".join(["<b>Now, everything you write here will be forwarded ",
                              "to admins. Then, they can contact you directly or via me if needed</b>",
                              "<i>send /finish to end feedback massage</i>"]),
                     reply_markup=feedback_keyboard
                     )
    await Menu.feedback.set()


async def exit_feedback(msg: Message):
    await msg.answer("<b>We are in main menu</b>", reply_markup=main_menu_keyboard)
    await Menu.in_main_menu.set()


async def about_us(msg: Message):
    await msg.answer("<b> We are bla bla bla...</b>", reply_markup=about_us_keyboard)

    await Menu.about_us.set()


async def exit_about_us(msg: Message):
    await msg.answer("<b>We are in main menu</b>", reply_markup=main_menu_keyboard)
    await Menu.in_main_menu.set()


async def exit_settings(msg: Message):
    await msg.answer("<b>Oh #%&*, here we go again!</b>",
                     reply_markup=main_menu_keyboard)
    await Menu.in_main_menu.set()


async def find_car_owner(msg: Message):

    await msg.answer("<b>Tap here to start searching a driver</b>", reply_markup=search_driver_keyboard)

    await Menu.search_student.set()

def user_menu_handlers(dp: Dispatcher):
    dp.register_message_handler(settings, text="Settings⚙️", state=Menu.in_main_menu, in_db=True)
    dp.register_message_handler(exit_settings, text=["Exit", "Back", "Finish"], state=Menu, in_db=True)

    dp.register_message_handler(feedback, text="Feedback🛎", state=Menu.in_main_menu, in_db=True)
    dp.register_message_handler(exit_feedback, text="Finish", state=Menu.feedback, in_db=True)

    dp.register_message_handler(about_us, text="About us™️", state=Menu.in_main_menu, in_db=True)
    dp.register_message_handler(exit_about_us, text="Back", state=Menu.about_us, in_db=True)
    dp.register_message_handler(find_car_owner, text="Find a car owner🔎", state=Menu.in_main_menu, in_db=True)
