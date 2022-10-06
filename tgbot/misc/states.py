from aiogram.dispatcher.filters.state import StatesGroup, State


class AdminStates(StatesGroup):
    selecting_partner_for_chatting = State()
    in_admin_panel = State()
    search_car = State()
    search_driver = State()
    chat = State()
    in_discussion_with_reporter = State()


class RegisterUser(StatesGroup):
    insert_car_number = State()
    insert_phone_number = State()


class DiscussionRoom(StatesGroup):
    join_room = State()
    in_room = State()


class Menu(StatesGroup):
    in_main_menu = State()

    search_number = State()
    start_chat = State()
    in_discussion = State()

    car_settings = State()
    add_car = State()
    edit_car = State()

    phone_settings = State()

    feedback = State()
    about_us = State()

    in_discussion_with_admin = State()

    share_discussion = State()

