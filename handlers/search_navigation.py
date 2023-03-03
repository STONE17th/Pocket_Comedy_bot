from aiogram.types import Message, InputFile, CallbackQuery, InputMediaPhoto
from loader import dp, db
from keyboards.callback import main_menu
from keyboards.inline import kb_search_filter, create_kb_navigation
from config import system_pictures
# from keyboards import kb_main_menu, main_menu
# from aiogram.utils.markdown import hbold, hlink, hitalic, hunderline, hstrikethrough


@dp.callback_query_handler(main_menu.filter(status='search_geo'))
async def search_geo(call: CallbackQuery):
    current_id = call.data.split(':')[-1]
    name = call.message.chat.full_name
    current_chat_id = call.message.chat.id
    current_message_id = call.message.message_id
    photo = system_pictures.get('no_events')
    caption = f'{name}, выбери город из списка:'
    await dp.bot.edit_message_media(media=InputMediaPhoto(media=photo,
                                                          caption=caption),
                                    chat_id=current_chat_id,
                                    message_id=current_message_id,
                                    reply_markup=create_kb_navigation(int(current_id) if current_id.isdigit() else 0,
                                                                      'search_geo'))

@dp.callback_query_handler(main_menu.filter(button='search_date'))
async def search_date(call: CallbackQuery):
    name = call.message.chat.full_name
    current_chat_id = call.message.chat.id
    current_message_id = call.message.message_id
    photo = system_pictures.get('main')
    caption = f'{name}, выбери фильтр для поиска:'
    await dp.bot.edit_message_media(media=InputMediaPhoto(media=photo,
                                                          caption=caption),
                                    chat_id=current_chat_id,
                                    message_id=current_message_id,
                                    reply_markup=create_kb_navigation(1, 'date', 1))

@dp.callback_query_handler(main_menu.filter(button='search_org'))
async def search_org(call: CallbackQuery):
    name = call.message.chat.full_name
    current_chat_id = call.message.chat.id
    current_message_id = call.message.message_id
    photo = system_pictures.get('main')
    caption = f'{name}, выбери фильтр для поиска:'
    await dp.bot.edit_message_media(media=InputMediaPhoto(media=photo,
                                                          caption=caption),
                                    chat_id=current_chat_id,
                                    message_id=current_message_id,
                                    reply_markup=create_kb_navigation(1, 'org', 1))

@dp.callback_query_handler(main_menu.filter(button='search_org'))
async def search_location(call: CallbackQuery):
    city = call.data.split(':')[-1]
    name = call.message.chat.full_name
    current_chat_id = call.message.chat.id
    current_message_id = call.message.message_id
    photo = system_pictures.get('main')
    caption = f'{name}, выбери фильтр для поиска:'
    await dp.bot.edit_message_media(media=InputMediaPhoto(media=photo,
                                                          caption=caption),
                                    chat_id=current_chat_id,
                                    message_id=current_message_id,
                                    reply_markup=create_kb_navigation(city, 'search_location'))