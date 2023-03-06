from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.callback import menu_main, menu_navigation
from loader import db


def create_kb_search_event(city: str, name: str, current_id: int):
    kb_search_event = InlineKeyboardMarkup(row_width=2)
    location_id = db.get_location_id(city=city, name=name)[0]
    list_events = db.get_all_events_in_location(location_id)
    next_id = int(current_id) + 1
    prev_id = int(current_id) - 1
    if current_id == 0:
        prev_id = len(list_events) - 1
    elif current_id == len(list_events) - 1:
        next_id = 0

    btn_join = InlineKeyboardButton(text='Записаться', callback_data=menu_main.new(menu='main',
                                                                              button='back'))

    btn_unjoin = InlineKeyboardButton(text='Выписаться', callback_data=menu_main.new(menu='main',
                                                                              button='back'))

    btn_back = InlineKeyboardButton(text='Назад', callback_data=menu_main.new(menu='main',
                                                                              button='back'))

    btn_prev = InlineKeyboardButton(text='<<<', callback_data=menu_select.new(menu='search_event',
                                                                              city=city,
                                                                              name=name,
                                                                              current_id=prev_id))
    btn_next = InlineKeyboardButton(text='>>>', callback_data=menu_select.new(menu='search_event',
                                                                              city=city,
                                                                              name=name,
                                                                              current_id=next_id))

    kb_search_event.row(btn_prev, btn_join, btn_next)
    kb_search_event.row(btn_back)

    return kb_search_event
