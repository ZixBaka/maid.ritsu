from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

main_car_inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Check my cars", switch_inline_query_current_chat="My Cars")],
    [InlineKeyboardButton(text="Add a car", callback_data="add_car")],
    [InlineKeyboardButton(text="Close", callback_data="close_car")]
])

search_driver_keyboard = InlineKeyboardMarkup(inline_keyboard=([
    [InlineKeyboardButton("Search🔎", switch_inline_query_current_chat="")],
    [InlineKeyboardButton(text="Cancel", callback_data="cancel_searching")]]))

car_callback = CallbackData("car", "method", "number")


def found_driver_keyboard(car_number: str):
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton("Start chatting",
                             callback_data=car_callback.new(method="send", number=car_number))],
        InlineKeyboardButton("Cancel",
                             callback_data="cancel_chatting")

    ])


def separate_car_inline_keyboard(car_number: str):
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="Edit this car", callback_data=car_callback.new(method="edit", number=car_number),),
        InlineKeyboardButton(text="Delete this car", callback_data=car_callback.new(method="delete", number=car_number))
    ]])



