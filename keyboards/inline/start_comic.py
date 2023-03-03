from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.callback import main_menu

kb_main_menu_comic = InlineKeyboardMarkup(row_width=2)

kb_no_events = InlineKeyboardMarkup(row_width=2)

btn_search_events = InlineKeyboardButton(text='Поиск',
                                         callback_data=main_menu.new(menu='main',
                                                                     status='comic',
                                                                     button='search'))
btn_my_events = InlineKeyboardButton(text='Мои события',
                                     callback_data=main_menu.new(menu='main',
                                                                 status='comic',
                                                                 button='my_events'))
btn_settings = InlineKeyboardButton(text='Настройки',
                                    callback_data=main_menu.new(menu='main',
                                                                status='comic',
                                                                button='settings'))

btn_back = InlineKeyboardButton(text='В главное меню',
                                    callback_data=main_menu.new(menu='main',
                                                                status='comic',
                                                                button='back'))

kb_no_events.row(btn_search_events, btn_back)

kb_main_menu_comic.row(btn_search_events, btn_my_events)
kb_main_menu_comic.row(btn_settings)