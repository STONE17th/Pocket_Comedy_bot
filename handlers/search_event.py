from aiogram.types import Message, InputFile, CallbackQuery, InputMediaPhoto
from loader import dp, db
from keyboards.callback import select_event
from keyboards.inline import create_kb_search_event
from .search_navigation import parse_callback


@dp.callback_query_handler(select_event.filter(menu='select'))
async def search_geo(call: CallbackQuery):
    data = parse_callback(call.data)
    events_list = []
    if data.get('location'):
        location_id = db.get_location_id(city=data.get('city'), name=data.get('location'))[0]
        events_list = db.get_all_events_by(location_id=location_id)
        pass
    if data.get('date'):
        events_list = db.get_all_events_by(date=data.get('date'))
    if data.get('org_id'):
        events_list = db.get_all_events_by(user_id=data.get('org_id'))
    print(events_list)
    for event in events_list:

    # location_id = db.get_location_id(city=city, name=place)[0]
    # list_events = db.get_all_events_in_location(location_id)
    # current_chat_id = call.message.chat.id
    # current_message_id = call.message.message_id
    # photo = list_events[current_id][2]
    # caption = f'Название: {list_events[current_id][1]}\nОписание: {list_events[current_id][3]}\n' \
    #           f'Площадка: {place} ({city})\n' \
    #           f'Дата: {list_events[current_id][6]}\nЦена: {list_events[current_id][7]} руб'
    # await dp.bot.edit_message_media(media=InputMediaPhoto(media=photo, caption=caption),
    #                                 chat_id=current_chat_id,
    #                                 message_id=current_message_id,
    #                                 reply_markup=create_kb_search_event(city, place, current_id))
