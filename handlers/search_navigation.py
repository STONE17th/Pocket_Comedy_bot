from aiogram.types import CallbackQuery, InputMediaPhoto
from loader import dp
from keyboards.callback import menu_search, select_event
from keyboards.inline import create_kb_navigation
from config import system_pictures


@dp.callback_query_handler(select_event.filter(menu=['city', 'date', 'org', 'event']))
@dp.callback_query_handler(menu_search.filter(menu='search'))
async def select_filter(call: CallbackQuery):
    call_data = {}
    if call.data.split(':')[0] == 'SelectEvent':
        call_data = parse_callback(call.data)
    else:
        call_data['menu'] = call.data.split(':')[-1]
    name = call.message.chat.full_name
    current_chat_id = call.message.chat.id
    current_message_id = call.message.message_id
    photo = caption = ''

    match call_data['menu']:
        case 'city':
            photo = system_pictures.get('main')
            caption = f'{name}, выбери город из списка:'
        case 'date':
            photo = system_pictures.get('main')
            caption = f'{name}, выбери нужную дату:'
        case 'org':
            photo = system_pictures.get('main')
            caption = f'{name}, выбери организатора:'
        case 'event':
            photo = system_pictures.get('main')
            caption = f'{name}, выбери организатора:'

    await dp.bot.edit_message_media(media=InputMediaPhoto(media=photo, caption=caption),
                                    chat_id=current_chat_id,
                                    message_id=current_message_id,
                                    reply_markup=create_kb_navigation(call_data))


def parse_callback(data: str) -> dict:
    data = data.split(':')
    data_dict = {'menu': data[1], 'location': data[2], 'city': data[3],
                 'org_id': int(data[4]), 'date': data[5],
                 'current_id': int(data[6])}
    return data_dict
