from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


inline_go_kb = InlineKeyboardMarkup()
inline_go_kb.add(
    InlineKeyboardButton('Go▶', callback_data='start_register')
)

inline_additional_confirm = InlineKeyboardMarkup()
inline_additional_confirm.add(
    InlineKeyboardButton("✅Yeah", callback_data='extra'),
    InlineKeyboardButton("❌No", callback_data='no_extra')
)


contact = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
contact.add(
    KeyboardButton('☎Send my number', request_contact=True),
    KeyboardButton('🙅‍♂️I prefer not to report it')
)


inline_delete_confirm = InlineKeyboardMarkup(row_width=1)
inline_delete_confirm.add(
    InlineKeyboardButton("🗑Yes, i want to clear my data", callback_data='delete_user'),
    InlineKeyboardButton('🔙Back', callback_data='no_delete')
)