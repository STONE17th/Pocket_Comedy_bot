from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.callback import main_menu

kb_search_filter = InlineKeyboardMarkup(row_width=2)

btn_search_geo = InlineKeyboardButton(text='По геолокации',
                                         callback_data=main_menu.new(menu='search',
                                                                     status='search_geo',
                                                                     button=0))
btn_search_date = InlineKeyboardButton(text='По дате',
                                     callback_data=main_menu.new(menu='search',
                                                                 status='comic',
                                                                 button='search_date'))
btn_search_org = InlineKeyboardButton(text='По организатору',
                                    callback_data=main_menu.new(menu='search',
                                                                status='comic',
                                                                button='search_org'))

btn_back = InlineKeyboardButton(text='Назад',
                                    callback_data=main_menu.new(menu='search',
                                                                status='comic',
                                                                button='back'))


kb_search_filter.row(btn_search_geo, btn_search_date, btn_search_org)
kb_search_filter.row(btn_back)