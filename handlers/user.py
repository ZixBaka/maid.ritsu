from aiogram.dispatcher import Dispatcher
from aiogram.types import Message, ParseMode, CallbackQuery
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from bot.keyboards.user_register_inline import inline_go_kb, inline_additional_confirm, contact
from bot.filters.valid_number import is_valid
from bot.database.main_db import insert_new_db


class FsmRegister(StatesGroup):
    main_number = State()
    extra = State()
    extra2 = State()
    phone = State()


async def start_msg(msg: Message):
    hello_text = f"🇬🇧Hello <i>{msg.from_user.first_name}</i>!\n" \
                 f"This bot will help you to find owner of parked car🚘\n" \
                 f"<b>Let's register together!</b>"
    await msg.answer(hello_text, parse_mode=ParseMode.HTML, reply_markup=inline_go_kb)


async def register_start(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(f"Great! Please, send me your car's number\n"
                                  f"<i>(Example: <b>01M777BA</b>)</i>", parse_mode=ParseMode.HTML)
    await FsmRegister.main_number.set()


async def first_number(msg: Message, state=FSMContext):
    async with state.proxy() as data:
        data['main'] = msg.text
        data['extra'] = None
        data['extra2'] = None
        data['contact'] = None
    await msg.answer('👍Awesome, do you want to add extra car?', reply_markup=inline_additional_confirm)


# finishes registration
async def write_data(msg: Message, state=FSMContext, number=None):
    async with state.proxy() as data:
        data['contact'] = number
        await insert_new_db(msg.chat.id, data['main'], data['extra'], data['extra2'], data['contact'])
    await msg.answer(f'🥳Your data were saved successfully\n'
                     f'🚙Your car number(s):\n'
                     f'<code>{data["main"]}</code>'
                     f'<code>{" " + x if (x := data["extra"]) is not None else ""}</code>'
                     f'<code>{" " + y if (y := data["extra2"]) is not None else ""}</code>\n'
                     f'Your contact: <i>{data["contact"]}</i>',
                     parse_mode=ParseMode.HTML)
    await state.finish()


# contact get
async def enter_phone(callback: CallbackQuery):
    await callback.message.delete()
    await FsmRegister.phone.set()
    await callback.message.answer('📞Nice, I need your contact (Optional)',
                                  reply_markup=contact)
    await callback.answer()


async def number_get(msg: Message):
    await write_data(msg, number=msg.contact.phone_number)

"""Extra number's section"""


# extra number 1
async def extra_info(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('🤑Alright rich guy/ lady, send me another one')


def register_user(dp: Dispatcher):
    dp.register_message_handler(start_msg, commands='start')
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
    dp.register_message_handler(number_get, state=FsmRegister.phone, content_types='contact')
    # extra numbers
