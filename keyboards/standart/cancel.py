from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

kb_cancel = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

btn_cancel = KeyboardButton(text='Отмена')

kb_cancel.add(btn_cancel)