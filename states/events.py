from aiogram.dispatcher.filters.state import StatesGroup, State


class Event(StatesGroup):
    name = State()
    poster = State()
    description = State()
    city_loca = State()
    name_loca = State()
    address_loca = State()
    phone_loca = State()
    url_loca = State()
    confirm_loca = State()
    date = State()
    price = State()
    confirm = State()