from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.callback import menu_search, select_event
from loader import db


def create_kb_event_navigation(data: dict, join_button: str, user_id: int):
    kb_search_event = InlineKeyboardMarkup(row_width=2)
    events_list = []
    prev_menu = ''

    if data.get('location'):
        location_id = db.get_location_id(city=data.get('city'), name=data.get('location'))[0]
        events_list = db.get_all_events_by(location_id=location_id)
        prev_menu = 'event'
    if data.get('date'):
        events_list = db.get_all_events_by(date=data.get('date'))
        prev_menu = 'date'
    if data.get('org_id'):
        events_list = db.get_all_events_by(user_id=data.get('org_id'))
        prev_menu = 'org'
    if not data.get('city') or data.get('menu') == 'my_events':
        events_list = db.user_events(user_id)
    meta_cur = data.get('current_id', 0)
    if isinstance(meta_cur, int):
        current_id = int(meta_cur)
    else:
        current_id = int(meta_cur.split()[1])
    next_id = current_id + 1
    prev_id = current_id - 1
    if current_id == 0:
        prev_id = len(events_list) - 1
    elif current_id == len(events_list) - 1:
        next_id = 0

    btn_join = InlineKeyboardButton(text=join_button, callback_data=select_event.new(menu='ev',
                                                                                     location=data.get('location', ''),
                                                                                     city=data.get('city', ''),
                                                                                     org_id=data.get('org_id', 0),
                                                                                     date=data.get('date', ''),
                                                                                     current_id=f'add {current_id}'))

    # btn_back = InlineKeyboardButton(text='Назад', callback_data=menu_main.new(menu='main',
    #                                                                           button='back'))
    if data.get('city') and not data.get('location'):
        btn_back = InlineKeyboardButton(text='По геолокации',
                                        callback_data=menu_search.new(menu='search',
                                                                      button='city'))
    elif not (data.get('city') and data.get('org_id') and data.get('date')):
        btn_back = InlineKeyboardButton(text='В главное меню',
                                        callback_data=menu_search.new(menu='main',
                                                                      button='main'))
    else:
        btn_back = InlineKeyboardButton(text='Назад', callback_data=select_event.new(menu=prev_menu,
                                                                                     location='',
                                                                                     city=data.get('city', ''),
                                                                                     org_id=data.get('org_id', 0),
                                                                                     date=data.get('date', ''),
                                                                                     current_id=0))
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
