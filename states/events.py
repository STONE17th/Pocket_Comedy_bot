from aiogram.dispatcher.filters.state import StatesGroup, State


class Event(StatesGroup):
    name = State()
    poster = State()
    description = State()
    location = State()
    date = State()
    price = State()
    confirm = State()