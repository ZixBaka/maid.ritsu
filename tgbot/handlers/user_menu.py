from aiogram import Dispatcher
from aiogram.types import CallbackQuery, Message
from aiogram.dispatcher import FSMContext

from tgbot.keyboards.inline import settings_keyboard, about_us_keyboard, \
    main_menu_keyboard, feedback_keyboard_after, report_keyboad
from tgbot.misc.states import Menu
from tgbot.models.cars import Car


async def settings(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text(
        "".join(["<b> In this section, you can manage</b>"
                 "<b> information that related to you.</b>"]),
        reply_markup=settings_keyboard)
    await call.answer()


async def feedback(call: CallbackQuery):
    await call.message.edit_text("".join(["<b>Now, everything you write here will be forwarded ",
                                          "to admins. Then, they can contact you directly or via bot if needed</b>"
                                          ]),
                                 reply_markup=feedback_keyboard_after,
                                 )
    await Menu.feedback.set()
    await call.answer()


async def about_us(call: CallbackQuery):
    await call.message.edit_text(f"𝐖𝐈𝐔𝐓 𝐏𝐚𝐫𝐤𝐢𝐧𝐠 𝐛𝐨𝐭\n"
                                 f"This bot exists thankfully for those who contributed\n"
                                 f"this <a href='https://github.com/mad-maids/maid.ritsu'>project</a>"
                                 f", and they are:\n\n"
                                 f"👨‍💻<a href='https://github.com/Azizbek-B'>Azizbek</a> (Co-Creator, Maintainer)\n"
                                 f"🕵️‍♂<a href='https://t.me/muminovbob'>Bobomurod</a> (Co-Creator, Maintainer)\n"
                                 f"👩‍🚀<a href='https://github.com/uwussimo'>UwUssimo</a> (Core Contributor)\n\n"
                                 f"Copyright © 2022 <a href='https://github.com/mad-maids'>Mad Maids</a>",
                                 reply_markup=about_us_keyboard,
                                 disable_web_page_preview=True)
    await call.answer()


async def exit_to_menu(call: CallbackQuery, state: FSMContext):
    await state.finish()
    cars = await Car.get_all_by_tg(call.bot.get("db"), call.from_user.id)
    car = []
    for r in cars:
        car.append(r.car_number)
    await call.message.edit_text(f"👤𝐍𝐚𝐦𝐞: <b>{call.from_user.first_name}</b>\n"
                                 f"🚙𝐂𝐚𝐫(𝐬): <code>{'</code><code> '.join(car)}</code>",
                                 reply_markup=main_menu_keyboard)
    await call.answer()


async def exit_to_menu_after(call: CallbackQuery, state: FSMContext):
    await state.finish()
    cars = await Car.get_all_by_tg(call.bot.get("db"), call.from_user.id)
    car = []
    for r in cars:
        car.append(r.car_number)
    await call.message.delete_reply_markup()
    await call.message.edit_text('Thank you for feedback!❤')
    await call.message.answer(f"👤𝐍𝐚𝐦𝐞: <b>{call.from_user.first_name}</b>\n"
                              f"🚙𝐂𝐚𝐫(𝐬): <code>{'</code><code> '.join(car)}</code>",
                              reply_markup=main_menu_keyboard)


async def close_menu(call: CallbackQuery):
    await call.message.delete()


async def helper(msg: Message):
    help_text = f"<b>HOW TO USE THE BOT</b>❓\n\n<i>" \
                f"1. Register your car\n" \
                f"2. Send /search\n" \
                f"3. Send the number of the car you want to find\n" \
                f"4. Enjoy your results☺\n</i>" \
                f"\n\n" \
                f"<b>PRIVACY INFO🔒</b>\n\n<i>" \
                f"🌐 Your Telegram user or id won't be shared\n\n" \
                f"📞 Adding a phone number is optional, but if you add a number," \
                f" others will be able to see it\n\n" \
                f"🤡 If you are being spammed, send the spammer's machine number via /me > Feedback</i>\n\n" \
                f"⚠Using the bot for other purposes\n" \
                f"(spam, fraud) is punishable by a <b>BAN</b>"
    await msg.answer(help_text)


async def reporter(msg: Message):
    text = "<code>If you have been faced on of the troubles below, \n" \
           "please, choose related one and admins will do their best to solve it!</code>"
    await msg.answer(text, reply_markup=report_keyboad)


def user_menu_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(settings, text="settings", in_db=True, call_is_private=True)
    dp.register_callback_query_handler(about_us, text="about", in_db=True, call_is_private=True)
    dp.register_callback_query_handler(feedback, text="feedback", in_db=True, call_is_private=True)
    dp.register_callback_query_handler(exit_to_menu_after, text="back_to_menu_after", state=["*", "", None])
    dp.register_callback_query_handler(exit_to_menu, text="back_to_menu", state=["*", "", None])
    dp.register_callback_query_handler(close_menu, text='hide_menu', in_db=True, call_is_private=True)
    dp.register_message_handler(helper, state=["*", ""], commands='help', in_db=True, is_private=True)
    dp.register_message_handler(reporter, state=["*", ""], commands='report', in_db=True, is_private=True)
