from aiogram.types import Message, InputFile, CallbackQuery, InputMediaPhoto
from loader import dp, db
from keyboards.callback import select_event
from keyboards.inline import create_kb_event_navigation
from .search_navigation import parse_callback


@dp.callback_query_handler(select_event.filter(menu=['my_events', 'ev', 'select']))
async def show_current_event(call: CallbackQuery):
    call_data = parse_callback(call.data)
    events_list = []
    if call_data.get('location'):
        location_id = db.get_location_id(city=call_data.get('city'),
                                         name=call_data.get('location'))[0]
        events_list = db.get_all_events_by(location_id=location_id)
        pass
    elif call_data.get('date'):
        events_list = db.get_all_events_by(date=call_data.get('date'))
    elif call_data.get('org_id'):
        events_list = db.get_all_events_by(user_id=call_data.get('org_id'))
        print(events_list)
    elif not call_data.get('city') or call_data.get('menu') == 'my_events':
        events_id_list = list(map(lambda x: x[0], db.user_events(call.from_user.id)))
        events_list = [db.get_all_events_by(event_id=event_id)[0] for event_id in events_id_list]
    id_is_num = call_data.get('current_id')
    current_id = int(id_is_num) if isinstance(id_is_num, int) else int(str(id_is_num).split()[1])

    data = from_tuple_to_dict(events_list[current_id])
    current_chat_id = call.message.chat.id
    current_message_id = call.message.message_id
    comics_id_list = list(map(lambda x: x[0], db.get_comics(data.get('event_id'))))
    if str(id_is_num).split()[0] == 'add':
        if call.from_user.id in comics_id_list:
            db.remove_comic(call.from_user.id, data.get('event_id'))
        else:
            db.add_comic(call.from_user.id, data.get('event_id'))

    comics_id_list = list(map(lambda x: x[0], db.get_comics(data.get('event_id'))))
    join_button = 'Выписаться' if call.from_user.id in comics_id_list else 'Записаться'
    comics_id_list = [db.get_user_name(user_id)[0] for user_id in comics_id_list]

    comics = '\n'.join([f'{i}. {comic}' for i, comic in enumerate(comics_id_list, 1)])
    photo = data.get('poster')
    caption = f"{current_id + 1}/{len(events_list)}\n" \
              f"Название: {data.get('name')}\nОписание: {data.get('description')}\n" \
              f"Площадка: {data.get('location')} ({data.get('city')})\n" \
              f"Дата: {data.get('date')}\nЦена: {data.get('price')} руб\n\n" \
              f"Выступают:\n{comics}"
    await dp.bot.edit_message_media(media=InputMediaPhoto(media=photo, caption=caption),
                                    chat_id=current_chat_id,
                                    message_id=current_message_id,
                                    reply_markup=create_kb_event_navigation(call_data, join_button,
                                                                            call.from_user.id))


def from_tuple_to_dict(data: tuple) -> dict:
    data = list(data)
    _, name, city, _, _, _ = db.get_location(int(data[4]))[0]
    return {'event_id': int(data[0]), 'name': data[1], 'poster': data[2],
            'description': data[3], 'city': city, 'location': name,
            'org_id': data[5], 'date': data[6], 'price': data[7]}
