from aiogram.types import Message, ParseMode, CallbackQuery
from aiogram.dispatcher import Dispatcher
from keyboards.user_register_inline import inline_delete_confirm
from database.main_db import delete_user_db, user_info_db
from helper import bot
from asyncio import gather


# delete user
async def confirm_delete(msg: Message):
    warning_text = f"<b>⚠Be careful!</b>\n" \
                   f"After deleting the data, you will not be able to use the Bot's services." \
                   f" <i>(You will need to register again)</i>"
    await msg.reply(warning_text, reply_markup=inline_delete_confirm,
                    parse_mode=ParseMode.HTML)


async def back(callback: CallbackQuery):
    await callback.message.delete()
    await bot.delete_message(callback.message.chat.id, callback.message.message_id-1)


async def delete_user(callback: CallbackQuery):
    await delete_user_db(callback.message.chat.id)
    await callback.answer('🟢Your data has been deleted successfully🗑', show_alert=True)
    await back(callback)


# user info
async def user_info(msg: Message):
    await (user_data := gather(user_info_db(msg.from_user.id)))
    user_data = user_data.result()[0]
    try:
        info_text = f'👤Your name: {msg.from_user.first_name}\n' \
                    f'🚘Your car number(s):\n' \
                    f'<code>{user_data[1]}</code>' \
                    f'<code>{" " + x if (x := user_data[2]) is not None else ""}</code>' \
                    f'<code>{" " + y if (y := user_data[3]) is not None else ""}</code>\n' \
                    f'📞Your contact: <i>{user_data[4]}</i>'
        await msg.answer(info_text, parse_mode=ParseMode.HTML)
    except TypeError:
        await msg.answer('🙏Please, register first\n'
                         '💬Using /register')


# help message
async def help_info(msg: Message):
    help_text = f"❓𝐈𝐧 𝐨𝐫𝐝𝐞𝐫 𝐭𝐨 𝐮𝐬𝐞 𝐭𝐡𝐞 𝐛𝐨𝐭\n" \
                f"1. Register\n" \
                f"2. Send the bot a number in the " \
                f"format <i>(01XXXYYY)</i>\n" \
                f"3. Bot would respond you🤖\n" \
                f"\n" \
                f"🧩𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬\n" \
                f"/restart - Restarts the bot\n" \
                f"/me - Personal info\n" \
                f"/register - (Re)writes your data\n" \
                f"/delete - Deletes your data\n" \

    await msg.answer(help_text, parse_mode=ParseMode.HTML)


async def about(msg: Message):
    about_text = f"𝐖𝐈𝐔𝐓 𝐏𝐚𝐫𝐤𝐢𝐧𝐠 𝐛𝐨𝐭\n" \
                 f"<i>This bot exists thankfully for those who contributed\n" \
                 f"this project, and they are:</i>\n" \
                 f"\n" \
                 f"👨‍💻<a href='https://t.me/muminovbob'>Bobomurod</a> (Creator, Maintainer)\n" \
                 f"👩‍🚀<a href='https://github.com/uwussimo'>UwUssimo</a> (Core Contributor)\n" \
                 f"\n" \
                 f"Copyright © 2022 <a href='https://github.com/mad-maids'>Mad Maids</a>"
    await msg.answer(about_text, parse_mode=ParseMode.HTML, disable_web_page_preview=True)


def register_user_commands(dp: Dispatcher):
    dp.register_message_handler(about, commands='about')
    dp.register_message_handler(confirm_delete, commands='delete')
    dp.register_message_handler(user_info, commands='me')
    dp.register_message_handler(help_info, commands='help')
    # query handlers
    dp.register_callback_query_handler(delete_user, text='delete_user')
    dp.register_callback_query_handler(back, text='no_delete')
