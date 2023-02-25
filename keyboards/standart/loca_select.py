from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from .cancel import btn_cancel
from loader import db


kb_loca_select = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

loca_list = [KeyboardButton(text=f'{loca[0]} ({loca[1]})') for loca in set(db.all_locations())]


kb_loca_select.add(*loca_list)
kb_loca_select.add(btn_cancel)