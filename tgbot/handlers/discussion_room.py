from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from tgbot.config import Config
from tgbot.keyboards.inline import found_driver_keyboard, car_callback, back_inline_car, feedback_keyboard, \
    found_driver_keyboard_extra, on_my_way, on_my_way_extra, notify_callback, ignore_callback, \
    report_agreement_keyboard, discussion_finish_keyboard, report_agreement_callback_data, discussion_finish_call_data
from tgbot.keyboards.admin_kb import admin_feedback_keyboard
from tgbot.misc.states import Menu
from tgbot.models.cars import Car
from tgbot.models.students import Student
from aiogram.utils.exceptions import BotBlocked
from tgbot.misc.states import AdminStates


# ============= FEEDBACK =====================
async def feedback_discussion(msg: Message):
    config: Config = msg.bot.get("config")
    await msg.reply('Your message has been sent👍')
    await msg.bot.send_message(
        config.tg_bot.admins_group,
        "".join([f"<b>From user:\n [<code>{msg.from_user.id}</code>]\n"
                 f" <a href='tg://user?id={msg.from_user.id}'>{msg.from_user.first_name}</a></b>\n\n",
                 f"<i>{msg.text}</i>"]
                ), reply_markup=admin_feedback_keyboard(msg.from_user.id))


async def discussion_with_admin(msg: Message):
    config: Config = msg.bot.get("config")

    await msg.bot.send_message(
        config.tg_bot.admins_group,
        "".join([f"<b>From user:\n [<code>{msg.from_user.id}</code>]\n"
                 f" <a href='tg://user?id={msg.from_user.id}'>{msg.from_user.first_name}</a></b>\n\n",
                 f"<i>{msg.text}</i>"]
                ))


async def discussion_with_admin_finish(msg: Message, state: FSMContext):
    config: Config = msg.bot.get("config")

    await msg.answer('Discussion was stopped')
    await state.finish()

    await state.storage.finish(chat=config.tg_bot.admins_group, user=config.tg_bot.admin_ids[0])
    await msg.bot.send_message(
        config.tg_bot.admins_group,
        "".join([f"<b>From user:\n [<code>{msg.from_user.id}</code>]\n"
                 f" <a href='tg://user?id={msg.from_user.id}'>{msg.from_user.first_name}</a></b>\n\n",
                 f"<code>User finished the conversation</code>"]
                ))


async def finish_discussion(msg: Message, state: FSMContext):
    data = await state.get_data()
    reporter = int(data.get("reporter"))

    await msg.bot.send_message(
        reporter,
        f"<b>🔴Admin decided to finish conversation </b>")

    await state.storage.finish(chat=reporter, user=reporter)
    await state.finish()


# ============= SEARCH =====================
async def start_search(msg: Message):
    await Menu.search_number.set()
    await msg.answer('👮‍♂Alright, please <b>send the number of the car</b> that prevents you from leaving the '
                     'parking lot', reply_markup=back_inline_car)


async def start_search_without_car(msg: Message, state: FSMContext):
    await Menu.search_number.set()
    await msg.answer('You can not search a car without having one!')
    await state.finish()


async def search_owner(msg: Message, cars: [Car]):
    for car in cars:
        session_maker = msg.bot.get("db")
        owner_id = await Car.get_owner_by_car(session_maker, car.car_number)
        number = await Student.get_number_by_tg(session_maker, owner_id)
        phone = f"📞𝐏𝐡𝐨𝐧𝐞 : <code>{number}</code>" if number is not None else ''
        await msg.answer(
                         f"🔹𝐓𝐡𝐞 𝐨𝐰𝐧𝐞𝐫 𝐡𝐚𝐬 𝐛𝐞𝐞𝐧 𝐟𝐨𝐮𝐧𝐝\n"
                         f"🚘𝐂𝐚𝐫 : <code>{msg.text.upper()}</code>\n"
                         f"{phone}",
                         reply_markup=found_driver_keyboard(car.car_number))
        return None
    else:
        await msg.answer('🔍The owner was not found😕')


async def stop_search(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.answer('🔻Search has stopped')
    await call.message.delete()


# ============= CHAT =====================

async def on_my_way_respond(call: CallbackQuery, callback_data: dict):
    r_car_number = callback_data.get("number")
    tg_id = callback_data.get("tg_id")

    respond_text = f"👤The owner is already heading to the car"
    await call.answer("🔔We have informed the requester")
    await call.message.edit_reply_markup(on_my_way_extra(r_car_number))
    await call.message.bot.send_message(tg_id, respond_text)


async def notify_user(call: CallbackQuery, callback_data: dict, state: FSMContext):
    car_number = callback_data.get("number")

    session_maker = call.bot.get("db")
    car_owner = await Car.get_car(session_maker, car_number)
    requester = await Car.get_car_by_tg(session_maker, int(call.from_user.id))

    await call.message.edit_reply_markup(found_driver_keyboard_extra(car_number))

    notify_text = f"👋Hello!\n" \
                  f"❗YOUR CAR <b>PREVENTS</b> ANOTHER CAR\n" \
                  f"❕FROM LEAVING THE PARKING LOT\n" \
                  f"\n" \
                  f"🙏Please come to your car\n" \
                  f"👤Request from: <code>{requester.car_number.upper()}</code>"
    try:
        await call.message.bot.send_message(car_owner.owner, notify_text, disable_web_page_preview=True,
                                            reply_markup=on_my_way(call.from_user.id, requester.car_number))
        await state.storage.set_state(chat=car_owner.owner, user=car_owner.owner, state=Menu.search_number)

        await call.answer('👮‍♂We have notified her/him🛎', show_alert=True)

    except BotBlocked:

        await call.message.answer("<code>Bot has been blocked by this user🤦‍♂️"
                                  "We are not able to connect you with such drivers</code>")
        await call.message.delete()
        await state.finish()


async def ignore_request(call: CallbackQuery, callback_data: dict, state: FSMContext):
    partner = callback_data.get("tg_id")
    await call.bot.send_message(partner, "💬The owner chose not to answer you🙁")
    await state.storage.finish(chat=partner, user=partner)

    await call.answer('You ignored them🫡')
    await state.finish()
    await call.message.delete()


# ============= CHAT =====================
async def cancel_searching(call: CallbackQuery, state: FSMContext):
    await call.message.answer('🔍Search has stopped🛑')
    await call.answer()
    await state.finish()
    await call.message.delete()


async def cancel_chatting(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    partner = data.get("partner")
    await call.bot.send_message(partner, "💬The dialogue was finished🛑", reply_markup=discussion_finish_keyboard)
    await state.storage.set_state(chat=partner, user=partner, state=Menu.share_discussion)
    await Menu.share_discussion.set()
    await call.message.answer('💬The dialogue was finished🛑', reply_markup=discussion_finish_keyboard)
    await call.message.delete()


async def start_chatting(call: CallbackQuery, callback_data: dict, state: FSMContext):
    car_number = callback_data.get("number")
    print(f'chat was started {callback_data.get("number")}')

    session_maker = call.bot.get("db")
    requester = await Car.get_car_by_tg(session_maker, call.from_user.id)

    start_text = f"🟢<b>The dialogue has begun</b>💬\n" \
                 f"<i>You can write messages and they will be\nsent to the owner of the car</i>"

    start_text_r = f"🟢<b>A driver(<code>{requester.car_number}</code>) started dialogue with you</b>💬\n" \
                   f"<i>You can write messages and they will be\nsent to the owner of the car</i>"
    try:
        await call.message.edit_text(start_text)
        await call.message.edit_reply_markup(feedback_keyboard)

        # owner
        car_owner = await Car.get_car(session_maker, car_number)

        await call.message.bot.send_message(car_owner.owner, start_text_r, reply_markup=feedback_keyboard)

        await state.storage.set_state(chat=car_owner.owner, user=car_owner.owner, state=Menu.start_chat.state)
        await state.storage.set_data(chat=car_owner.owner, user=car_owner.owner, data=dict(partner=call.from_user.id))

        await state.update_data(dict(partner=car_owner.owner))
        await Menu.start_chat.set()

    except BotBlocked:
        await call.message.answer('Partner blocked this bot')
        await state.finish()


async def send_message(msg: Message, state: FSMContext):
    data = await state.get_data()
    partner = data.get("partner")
    discussion_content = data.get("discussion_content")
    if discussion_content is None:
        discussion_content = ""
    txt_bubble = f"<a href='tg://user?id={msg.from_user.id}'>{msg.from_user.first_name}</a>" \
                 f"[<code>{msg.from_user.id}</code>]:\n" \
                 f"{msg.text}\n\n"

    discussion_content += txt_bubble
    partner_state = await state.storage.get_state(chat=partner, user=partner)
    partner_data = await state.storage.get_data(chat=partner, user=partner)
    await state.storage.update_data(chat=partner, user=partner,
                                    data=dict(discussion_content=discussion_content))
    await state.update_data(data=dict(discussion_content=discussion_content))
    if partner_state == Menu.start_chat.state:
        if partner_data.get("partner") == msg.from_user.id:
            await msg.bot.send_message(data.get("partner"),
                                       f"👤<b>Interlocutor</b>:\n\n<i>{msg.text}</i>\n"
                                       f"\n<b>[ /finish to end the dialog ]</b>")
        else:
            await msg.answer("This driver is chatting with another car driver, please try later👀")
            await state.finish()

    else:
        await msg.answer("<b>🔚Your Partner decided to end conversation😕</b>")
        await state.finish()


async def finish(msg: Message, state: FSMContext):
    data = await state.get_data()

    discussion_content = data.get("discussion_content")
    partner = data.get("partner")

    await msg.bot.send_message(partner, "💬The dialogue was finished🛑", reply_markup=discussion_finish_keyboard)

    await msg.answer('💬The dialogue was finished🛑', reply_markup=discussion_finish_keyboard)

    await state.storage.set_state(chat=partner, user=partner, state=Menu.share_discussion.state)
    await state.storage.set_data(chat=partner, user=partner, data=dict(discussion_content=discussion_content))

    await state.set_state(Menu.share_discussion.state)
    await state.update_data(dict(discussion_content=discussion_content))

    if discussion_content == "":
        await msg.answer("There is no point to report -_-")
        await msg.delete()
        await state.finish()


async def report(call: CallbackQuery):
    await call.message.edit_text("<b>Discussion history will be sent to administrators to identify violations.\n"
                                 "Do you agree?</b>", reply_markup=report_agreement_keyboard)


async def close(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.finish()


async def report_confirmation(call: CallbackQuery, callback_data: dict, state: FSMContext):
    answer = callback_data.get("answer")
    if answer == "yes":
        await call.answer("Discussion forwarded to admins, they will contact you ASAP.")
        config: Config = call.bot.get("config")
        data = await state.get_data()
        conversation = data.get("discussion_content")
        await call.bot.send_message(config.tg_bot.admins_group, text=conversation)

    elif answer == "no":
        await call.answer("You have decided no to report, discussion history is cleaned")
    await state.finish()
    await call.message.delete()


# ============= ERRORS =====================
async def error_late_start(call: CallbackQuery):
    await call.answer('🟡The chat has already started')


def discussion_handlers(dp: Dispatcher):

    # ========= FEEDBACK ==========
    dp.register_message_handler(feedback_discussion, state=Menu.feedback)
    dp.register_message_handler(finish_discussion, commands='finish', state=AdminStates.in_discussion_with_reporter)
    dp.register_message_handler(discussion_with_admin_finish, commands="finish", state=Menu.in_discussion_with_admin)
    dp.register_message_handler(discussion_with_admin, state=Menu.in_discussion_with_admin)

    # ========= Notify ==========
    dp.register_callback_query_handler(notify_user, car_callback.filter(method="notify"), state=Menu.search_number)
    dp.register_callback_query_handler(on_my_way_respond, notify_callback.filter(method='on_my_way'),
                                       state=Menu.search_number)

    dp.register_callback_query_handler(ignore_request, ignore_callback.filter(method='ignore'),
                                       state=Menu.search_number)
    # ========= CHAT ==========
    dp.register_message_handler(finish, commands="finish", state=[Menu.start_chat, AdminStates.chat])
    dp.register_callback_query_handler(cancel_chatting, text="back_to_menu",
                                       state=Menu.start_chat)
    dp.register_callback_query_handler(cancel_searching, text="cancel_chatting",
                                       state=Menu.search_number)

    dp.register_callback_query_handler(start_chatting, car_callback.filter(method="enter_room"),
                                       state=Menu.search_number)
    dp.register_message_handler(send_message, state=Menu.start_chat)

    # ======== ERRORS =========
    dp.register_callback_query_handler(error_late_start, car_callback.filter(method="enter_room"),
                                       state=Menu.start_chat)

    # ========= SEARCH ==========
    dp.register_message_handler(start_search, commands='search', in_db=True,
                                state="*", is_private=True, has_car=True)
    dp.register_message_handler(start_search_without_car, commands='search', in_db=True, state="*", is_private=True)

    dp.register_message_handler(search_owner, search_car=True, state=Menu.search_number)
    dp.register_callback_query_handler(stop_search, state=Menu.search_number, text='to_settings')

    dp.register_callback_query_handler(report, discussion_finish_call_data.filter(action="report"),
                                       state=Menu.share_discussion)
    dp.register_callback_query_handler(close, discussion_finish_call_data.filter(action="close"),
                                       state=[Menu.share_discussion, None])
    dp.register_callback_query_handler(report_confirmation, report_agreement_callback_data.filter(),
                                       state=Menu.share_discussion)
