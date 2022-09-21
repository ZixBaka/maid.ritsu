from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

main_car_inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Check my cars", switch_inline_query_current_chat="My Cars")],
    [InlineKeyboardButton(text="Add a car", callback_data="add_car")],
    [InlineKeyboardButton(text="Close", callback_data="close_car")]
])

car_callback = CallbackData("car", "method", "number")


def found_driver_keyboard(car_number: str):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Start chatting",
                              callback_data=car_callback.new(method="enter_room", number=car_number)),
         InlineKeyboardButton(text="Cancel",
                              callback_data="cancel_chatting")]])
    return keyboard


def separate_car_inline_keyboard(car_number: str):
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="Edit this car", callback_data=car_callback.new(method="edit", number=car_number),),
        InlineKeyboardButton(text="Delete this car", callback_data=car_callback.new(method="delete", number=car_number))
    ]])


main_menu_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Find a car owner🔎", switch_inline_query_current_chat="")],
                     [InlineKeyboardButton(text="Settings⚙️", callback_data="settings")],
                     [InlineKeyboardButton(text="About us™️", callback_data="about"),
                      InlineKeyboardButton(text="Feedback🛎", callback_data="feedback")]],
    resize_keyboard=True)


settings_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Cars", callback_data="my_cars"),
     InlineKeyboardButton(text="Phone", callback_data="my_phone")],
    [InlineKeyboardButton(text="Back", callback_data="back_to_menu")]],
    resize_keyboard=True)

about_us_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Exit", callback_data="back_to_menu")]],
    resize_keyboard=True
 )

feedback_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Finish", callback_data="back_to_menu")]],
    resize_keyboard=True
)
