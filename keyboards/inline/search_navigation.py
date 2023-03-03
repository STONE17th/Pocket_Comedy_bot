from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.callback import main_menu
from loader import db


def create_kb_navigation(current_id: int | str, target: str):
    kb_navigation = InlineKeyboardMarkup(row_width=2)
    target_list = []
    match target:
        case 'search_geo':
            target_list = db.all_cities()
        case 'search_location':
            target_list = db.all_locations()
        case 'search_date':
            pass
        case 'search_org':
            pass
    menu_list = []
    for item in target_list:
        menu_list.append(item[0])
    sorted_item_list = sorted(menu_list)
    menu_list.clear()
    count = 0
    row = []
    for item in sorted_item_list:
        if count < 6:
            row.append(item)
        else:
            count = 0
            menu_list.append(row)
            row = [item]
        count += 1
    else:
        menu_list.append(row)

    next_id = current_id + 1
    prev_id = current_id - 1
    if current_id == 0:
        prev_id = len(menu_list) - 1
    elif current_id == len(menu_list) - 1:
        next_id = 0
    buttons_list = []
    for button_item in menu_list[current_id]:
        buttons_list.append(InlineKeyboardButton(text=button_item, callback_data=main_menu.new(menu='search',
                                                                                  status='search_location',
                                                                                  button=button_item)))
    btn_back = InlineKeyboardButton(text='Назад', callback_data=main_menu.new(menu='search',
                                                                              status='search_geo',
                                                                              button='back'))
    btn_prev = InlineKeyboardButton(text='<<<', callback_data=main_menu.new(menu='search',
                                                                            status='search_geo',
                                                                            button=prev_id))
    btn_next = InlineKeyboardButton(text='>>>', callback_data=main_menu.new(menu='search',
                                                                            status='search_geo',
                                                                            button=next_id))

    kb_navigation.row(*buttons_list[:3])
    kb_navigation.row(*buttons_list[3:])
    kb_navigation.row(btn_prev, btn_back, btn_next)

    return kb_navigation
