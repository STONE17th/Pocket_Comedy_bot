from aiogram.types import Message, InputFile, CallbackQuery, InputMediaPhoto
from loader import dp, db
from keyboards.callback import select_event
from keyboards.inline import create_kb_event_navigation
from .search_navigation import parse_callback


@dp.callback_query_handler(select_event.filter(menu='ev'))
@dp.callback_query_handler(select_event.filter(menu='select'))
async def search_geo(call: CallbackQuery):
    call_data = parse_callback(call.data)
    events_list = []
    if call_data.get('location'):
        location_id = db.get_location_id(city=call_data.get('city'),
                                         name=call_data.get('location'))[0]
        events_list = db.get_all_events_by(location_id=location_id)
        pass
    if call_data.get('date'):
        events_list = db.get_all_events_by(date=call_data.get('date'))
    if call_data.get('org_id'):
        events_list = db.get_all_events_by(user_id=call_data.get('org_id'))
    current_id = int(call_data.get('current_id'))
    data = from_tuple_to_dict(events_list[current_id])
    current_chat_id = call.message.chat.id
    current_message_id = call.message.message_id
    photo = data.get('poster')
    caption = f"Название: {data.get('name')}\nОписание: {data.get('description')}\n" \
    f"Площадка: {data.get('location')} ({data.get('city')})\n" \
    f"Дата: {data.get('date')}\nЦена: {data.get('price')} руб"
    await dp.bot.edit_message_media(media=InputMediaPhoto(media=photo, caption=caption),
                                    chat_id=current_chat_id,
                                    message_id=current_message_id,
                                    reply_markup=create_kb_event_navigation(call_data))


def from_tuple_to_dict(data: tuple) -> dict:
    data = list(data)
    _, name, city, _, _, _ = db.get_location(int(data[4]))[0]
    return {'event_id': data[0], 'name': data[1], 'poster': data[2],
            'description': data[3], 'city': city, 'location': name,
            'org_id': data[5], 'date': data[6], 'price': data[7]}
