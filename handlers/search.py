from aiogram.types import Message, InputFile, CallbackQuery, InputMediaPhoto
from loader import dp, db
from keyboards.callback import menu_main
from keyboards.inline import kb_search_filter
from config import system_pictures


@dp.callback_query_handler(menu_main.filter(button='search'))
async def my_events(call: CallbackQuery):
    name = call.message.chat.first_name
    current_chat_id = call.message.chat.id
    current_message_id = call.message.message_id
    photo = system_pictures.get('main')
    caption = f'{name}, выбери фильтр для поиска:'
    await dp.bot.edit_message_media(media=InputMediaPhoto(media=photo, caption=caption),
                                    chat_id=current_chat_id,
                                    message_id=current_message_id,
                                    reply_markup=kb_search_filter)
