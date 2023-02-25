from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from .cancel import btn_cancel
from loader import db


kb_city_select = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

city_list = [KeyboardButton(text=city[0]) for city in set(db.all_cities())]


kb_city_select.add(*city_list)
kb_city_select.add(btn_cancel)