from aiogram.types import Message, InputFile, CallbackQuery, InputMediaPhoto
from loader import dp, db
from keyboards.callback import main_menu
from keyboards.inline import kb_main_menu_comic
from config import system_pictures
# from keyboards import kb_main_menu, main_menu
# from aiogram.utils.markdown import hbold, hlink, hitalic, hunderline, hstrikethrough


@dp.callback_query_handler(main_menu.filter(button='back'))
async def my_events(call: CallbackQuery):

    name = call.message.chat.full_name
    current_chat_id = call.message.chat.id
    current_message_id = call.message.message_id
    photo = system_pictures.get('main')
    caption = f'Привет, {name}!\nЯ скучал, че будем делать?'
    await dp.bot.edit_message_media(media=InputMediaPhoto(media=photo, caption=caption),
                                    chat_id=current_chat_id,
                                    message_id=current_message_id,
                                    reply_markup=kb_main_menu_comic)
