from loader import dp, db
from aiogram.types import Message, InputFile, CallbackQuery, InputMediaPhoto
from aiogram.dispatcher import FSMContext
from states import User
from keyboards.standart import kb_yes_no, kb_user_role, kb_city_select, kb_cancel
from keyboards.inline import kb_main_menu_comic
from keyboards.callback import menu_search
from config import system_pictures, admin_promo_code, comic_promo_code


@dp.callback_query_handler(menu_search.filter(menu='main'))
async def start_message(call: CallbackQuery, user_status: str):
    current_chat_id = call.message.chat.id
    current_message_id = call.message.message_id
    photo = system_pictures.get('main')
    caption = ''
    keyboard = kb_main_menu_comic
    if user_status == 'Admin':
        caption = f'Приветствую, {call.from_user.first_name}!\nТвоя роль Админ!'
        keyboard = kb_main_menu_comic

    elif user_status == 'Comic':
        caption = f'Приветствую, {call.from_user.first_name}!\nТвоя роль Комик!'
        keyboard = kb_main_menu_comic

    elif user_status == 'Guest':
        caption = f'Приветствую, {call.from_user.first_name}!\nТвоя роль Гость!'
        keyboard = kb_main_menu_comic

    await dp.bot.edit_message_media(media=InputMediaPhoto(media=photo, caption=caption),
                                    chat_id=current_chat_id,
                                    message_id=current_message_id,
                                    reply_markup=keyboard)


@dp.message_handler(commands=['start', 'старт', 'начать'], state=None)
async def start_message(message: Message, user_status: str):
    if user_status == 'Admin':
        await message.answer(f'Приветствую, {message.from_user.first_name}!\n'
                             'Твоя роль Админ!')
    elif user_status == 'Comic':
        await dp.bot.send_photo(chat_id=message.from_user.id,
                                photo=system_pictures.get('main'),
                                caption=f'Привет, {message.from_user.first_name}!\nЯ скучал, че будем делать',
                                reply_markup=kb_main_menu_comic)
    elif user_status == 'Guest':
        await message.answer(f'Приветствую, {message.from_user.first_name}!\n'
                             'Твоя роль Гость!')
    else:
        await message.answer(f'Приветствую, {message.from_user.first_name}!\n'
                             'Твой id в базе не найден. Давай его создадим\n'
                             'Введи свои Имя и Фамилию:', reply_markup=kb_cancel)
        await User.name.set()


@dp.message_handler(state=User.name)
async def enter_name(message: Message, state: FSMContext):
    await state.update_data({'name': message.text})
    await message.answer(f'Теперь выбери свою роль:', reply_markup=kb_user_role)
    await User.next()


@dp.message_handler(state=User.role)
async def enter_role(message: Message, state: FSMContext):
    if message.text == 'Организатор':
        await message.answer(f'Введите промо-код (его можно получить @STONECx3):', reply_markup=kb_cancel)
        await User.next()
    elif message.text == 'Комик':
        await message.answer(f'Введите промо-код (его можно получить @STONECx3):', reply_markup=kb_cancel)
        await User.next()
    elif message.text == 'Гость':
        await state.update_data({'role': 'Guest'})
        await message.answer(f'Введите номер телефона:', reply_markup=kb_cancel)
        await User.phone.set()
    else:
        await message.answer('Выберите роль: Организатор, Комик или Гость', reply_markup=kb_user_role)


@dp.message_handler(state=User.code)
async def enter_code(message: Message, state: FSMContext):
    if message.text in admin_promo_code:
        await state.update_data({'role': 'Admin'})
        await message.answer(f'Поздравляем! Твой статус Админ!\nВведи свой телефон:', reply_markup=kb_cancel)
        await User.next()
    elif message.text in comic_promo_code:
        await state.update_data({'role': 'Comic'})
        await message.answer(f'Поздравляем! Твой статус Комик!\nВведи свой телефон:', reply_markup=kb_cancel)
        await User.next()
    else:
        await message.answer(f'Введен неверный промо-код!\nВведите промо-код (его можно получить @STONECx3):',
                             reply_markup=kb_user_role)
        await User.role.set()


@dp.message_handler(state=User.phone)
async def enter_phone(message: Message, state: FSMContext):
    await state.update_data({'phone': message.text})
    await message.answer(f'Введи свой e-mail:', reply_markup=kb_cancel)
    await User.next()


@dp.message_handler(state=User.email)
async def enter_email(message: Message, state: FSMContext):
    await state.update_data({'email': message.text})
    await message.answer(f'Введи свой город:', reply_markup=kb_city_select)
    await User.next()


@dp.message_handler(state=User.city)
async def enter_city(message: Message, state: FSMContext):
    await state.update_data({'city': message.text})
    data = await state.get_data()
    message_text = f'Имя: {data["name"]}\nРоль: {data["role"]}\nТелефон: {data["phone"]}\n' \
                   f'EMail: {data["email"]}\nГород: {data["city"]}\n\nДанные введены верно?'
    await message.answer(message_text, reply_markup=kb_yes_no)
    await User.next()


@dp.message_handler(state=User.confirm)
async def enter_confirm(message: Message, user_status, state: FSMContext):
    if message.text == 'Да':
        data = await state.get_data()
        user = {"tg_id": message.from_user.id, "name": data["name"],
                "role": data["role"], "phone": data["phone"],
                "email": data["email"], "city": data["city"]}
        db.new_user(user)
        await state.finish()
        await start_message(message, user_status)
    else:
        await state.reset_data()
        await start_message(message, user_status)
