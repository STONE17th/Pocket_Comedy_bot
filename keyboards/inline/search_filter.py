from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.callback import menu_main, menu_search

kb_search_filter = InlineKeyboardMarkup(row_width=2)

btn_search_geo = InlineKeyboardButton(text='По геолокации',
                                      callback_data=menu_search.new(menu='search',
                                                                    button='city'))
btn_search_date = InlineKeyboardButton(text='По дате',
                                       callback_data=menu_search.new(menu='search',
                                                                     button='date'))
btn_search_org = InlineKeyboardButton(text='По организатору',
                                      callback_data=menu_search.new(menu='search',
                                                                    button='org'))

btn_back = InlineKeyboardButton(text='Назад',
                                callback_data=menu_main.new(menu='main',
                                                            button='back'))

kb_search_filter.row(btn_search_geo, btn_search_date, btn_search_org)
kb_search_filter.row(btn_back)
