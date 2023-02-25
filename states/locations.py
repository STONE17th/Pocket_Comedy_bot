from aiogram.dispatcher.filters.state import StatesGroup, State


class Location(StatesGroup):
    option = State()
    name = State()
    city = State()
    address = State()
    phone = State()
    url = State()
    confirm = State()