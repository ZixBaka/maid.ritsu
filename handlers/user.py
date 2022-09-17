""" Everything related with registration process"""
from aiogram.dispatcher import Dispatcher
from aiogram.types import Message, ParseMode, CallbackQuery
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from bot.keyboards.user_register_inline import inline_go_kb, inline_additional_confirm, contact
from bot.filters.valid_number import is_valid
from bot.database.main_db import insert_new_db, check_user_db
from aiogram.types import ReplyKeyboardRemove
from asyncio import gather


class FsmRegister(StatesGroup):
    main_number = State()
    extra = State()
    extra2 = State()
    phone = State()


async def extra_request(msg: Message):
    await msg.answer('👍Awesome, do you want to add extra car?', reply_markup=inline_additional_confirm)


async def start_msg(msg: Message, state=FSMContext):
    await (answer := gather(check_user_db(msg.from_user.id)))
    if answer.result()[0] is False:
        hello_text = f"🇬🇧Hello <i>{msg.from_user.first_name}</i>!\n" \
                     f"This bot will help you to find owner of parked car🚘\n" \
                     f"<b>Let's register together!</b>"
        await msg.answer(hello_text, parse_mode=ParseMode.HTML, reply_markup=inline_go_kb)
    else:
        await state.finish()
        await msg.answer(f'Hi {msg.from_user.first_name}')


async def register_again(msg: Message):
    await msg.answer('🔄Alright, do you want to update your data?', reply_markup=inline_go_kb)


async def register_start(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(f"Great! Please, send me your car's number\n"
                                  f"<i>(Example: <b>01M777BA</b>)</i>", parse_mode=ParseMode.HTML)
    await FsmRegister.main_number.set()


async def first_number(msg: Message, state=FSMContext):
    async with state.proxy() as data:
        data['main'] = msg.text.upper()
        data['extra'] = None
        data['extra2'] = None
        data['contact'] = None
    await extra_request(msg)


# finishes registration
async def write_data(msg: Message, state=FSMContext):
    async with state.proxy() as data:
        try:
            data['contact'] = msg.contact.phone_number
        except AttributeError:
            pass
        finally:
            await insert_new_db(msg.chat.id, data['main'], data['extra'], data['extra2'], data['contact'])
            await msg.answer(f'🥳Your data were saved successfully\n'
                             f'🚙Your car number(s):\n'
                             f'<code>{data["main"]}</code>'
                             f'<code>{" " + x if (x := data["extra"]) is not None else ""}</code>'
                             f'<code>{" " + y if (y := data["extra2"]) is not None else ""}</code>\n'
                             f'📞Your contact: <i>{data["contact"]}</i>',
                             parse_mode=ParseMode.HTML,
                             reply_markup=ReplyKeyboardRemove())
    await state.finish()


# contact get
async def enter_phone(callback: CallbackQuery):
    await callback.message.delete()
    await FsmRegister.phone.set()
    await callback.message.answer('📞Nice, I need your contact (Optional)',
                                  reply_markup=contact)
    await callback.answer()


"""Extra number's section"""


# extra number 1
async def extra_info(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('🤑Alright rich guy/ lady, send me another one')
    await FsmRegister.next()


async def extra_first(msg: Message, state=FSMContext):
    async with state.proxy() as data:
        data['extra'] = msg.text.upper()
    await extra_request(msg)


# extra 2
async def extra_second(msg: Message, state=FSMContext):
    async with state.proxy() as data:
        data['extra2'] = msg.text.upper()
    await FsmRegister.phone.set()
    await msg.answer('📞Nice, I need your contact (Optional)',
                     reply_markup=contact)


async def error_2(msg: Message):
    await msg.answer('⚠️Please write your data properly')


def register_user(dp: Dispatcher):
    dp.register_message_handler(start_msg, commands=['start', 'restart'],
                                state='*')
    dp.register_message_handler(register_again, commands='register')
    dp.register_callback_query_handler(register_start, text='start_register')
    # handle first number
    dp.register_message_handler(first_number,
                                lambda msg: is_valid(msg.text),
                                state=FsmRegister.main_number)
    # confirm / reject handle
    dp.register_callback_query_handler(enter_phone, state=FsmRegister, text='no_extra')
    # phone
    dp.register_message_handler(write_data, state=FsmRegister.phone,
                                text='🙅‍♂️I prefer not to report it')
    dp.register_message_handler(write_data, state=FsmRegister.phone, content_types='contact')
    # extra numbers
    dp.register_callback_query_handler(extra_info,
                                       state=[FsmRegister.main_number, FsmRegister.phone], text='extra')
    # extra 1
    dp.register_message_handler(extra_first, lambda msg: is_valid(msg.text),
                                state=FsmRegister.extra)
    # extra 2
    dp.register_callback_query_handler(extra_info, state=FsmRegister.extra, text='extra')
    dp.register_message_handler(extra_second, lambda msg: is_valid(msg.text),
                                state=FsmRegister.extra2)
    dp.register_message_handler(error_2, state=FsmRegister.states)
