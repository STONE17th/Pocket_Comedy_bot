from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.callback import menu_main, select_event
from loader import db


def create_kb_event_navigation(data: dict):
    kb_search_event = InlineKeyboardMarkup(row_width=2)
    events_list = []
    if data.get('location'):
        location_id = db.get_location_id(city=data.get('city'), name=data.get('location'))[0]
        events_list = db.get_all_events_by(location_id=location_id)
    if data.get('date'):
        events_list = db.get_all_events_by(date=data.get('date'))
    if data.get('org_id'):
        events_list = db.get_all_events_by(user_id=data.get('org_id'))
    current_id = int(data.get('current_id', 0))
    next_id = current_id + 1
    prev_id = current_id - 1
    if current_id == 0:
        prev_id = len(events_list) - 1
    elif current_id == len(events_list) - 1:
        next_id = 0

    btn_join = InlineKeyboardButton(text='Записаться', callback_data=menu_main.new(menu='main',
                                                                              button='back'))


    btn_back = InlineKeyboardButton(text='Назад', callback_data=menu_main.new(menu='main',
                                                                              button='back'))
    btn_prev = InlineKeyboardButton(text='<<<', callback_data=select_event.new(menu='ev',
                                                                               location=data.get('location', ''),
                                                                               city=data.get('city', ''),
                                                                               org_id=data.get('org_id', 0),
                                                                               date=data.get('date', ''),
                                                                               current_id=prev_id))
    btn_next = InlineKeyboardButton(text='>>>', callback_data=select_event.new(menu='ev',
                                                                               location=data.get('location', ''),
                                                                               city=data.get('city', ''),
                                                                               org_id=data.get('org_id', 0),
                                                                               date=data.get('date', ''),
                                                                               current_id=next_id))
    if len(events_list) > 1:
        kb_search_event.row(btn_prev, btn_join, btn_next)
    else:
        kb_search_event.row(btn_join)
    kb_search_event.row(btn_back)

    return kb_search_event
