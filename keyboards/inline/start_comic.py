from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.callback import menu_main, select_event

kb_main_menu_comic = InlineKeyboardMarkup(row_width=2)

kb_no_events = InlineKeyboardMarkup(row_width=2)

btn_search_events = InlineKeyboardButton(text='Поиск',
                                         callback_data=menu_main.new(menu='main',
                                                                     button='search'))
btn_my_events = InlineKeyboardButton(text='Мои события',
                                     callback_data=select_event.new(menu='my_events', location='', city='',
                                                                    org_id=0, date='', current_id=0))
btn_settings = InlineKeyboardButton(text='Настройки',
                                    callback_data=menu_main.new(menu='main',
                                                                button='settings'))

btn_back = InlineKeyboardButton(text='В главное меню',
                                callback_data=menu_main.new(menu='main',
                                                            button='back'))

kb_no_events.row(btn_search_events, btn_back)

kb_main_menu_comic.row(btn_search_events, btn_my_events)
kb_main_menu_comic.row(btn_settings)
