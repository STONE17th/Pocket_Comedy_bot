from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from .cancel import btn_cancel
from loader import db

def create_kb_loca_select(city: str):
    kb_loca_select = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    loca_list = [KeyboardButton(text=f'{loca[0]}') for loca in set(db.city_locations(city))]


    kb_loca_select.add(*loca_list)
    kb_loca_select.add(btn_cancel)
    return kb_loca_select
