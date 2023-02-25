from aiogram.dispatcher.filters.state import StatesGroup, State


class User(StatesGroup):
    name = State()
    role = State()
    phone = State()
    email = State()
    city = State()
    confirm = State()