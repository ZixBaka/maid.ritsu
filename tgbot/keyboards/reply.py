from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

phone_keyboard = ReplyKeyboardMarkup([[KeyboardButton("Share my contact", request_contact=True)], ["Cancel"]], resize_keyboard=True)

main_menu_keyboard = ReplyKeyboardMarkup([[KeyboardButton("Find a car owner🔎")], [KeyboardButton("Settings⚙️")],
                                          [KeyboardButton("About us™️"), KeyboardButton("Feedback🛎")]],
                                         resize_keyboard=True)

settings_keyboard = ReplyKeyboardMarkup([[KeyboardButton("Cars"), KeyboardButton("Phone")],
                                         [KeyboardButton("Back")]],
                                        resize_keyboard=True, one_time_keyboard=True)

about_us_keyboard = ReplyKeyboardMarkup([[KeyboardButton("Exit")]], resize_keyboard=True)

feedback_keyboard = ReplyKeyboardMarkup([[KeyboardButton("Finish")]], resize_keyboard=True)

