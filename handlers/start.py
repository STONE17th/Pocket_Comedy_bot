from loader import dp, db
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from states import User
from keyboards.standart import kb_yes_no, kb_user_role, kb_cancel


@dp.message_handler(commands=['start', 'старт', 'начать'], state=None)
async def start_message(message: Message):
    user_role = db.get_user_role(message.from_user.id)
    if user_role and user_role[0] == 'Админ':
        await message.answer(f'Приветствую, {message.from_user.first_name}!\n'
                             'Твоя роль Админ!')
    elif user_role and user_role[0] == 'Комик':
        await message.answer(f'Приветствую, {message.from_user.first_name}!\n'
                             'Твоя роль Комик!')
    elif user_role and user_role[0] == 'Гость':
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
    if message.text in ['Комик', 'Гость']:
        await state.update_data({'role': message.text})
        await message.answer(f'Введи свой номер телефона:', reply_markup=kb_cancel)
        await User.next()
    else:
        await message.answer('Выберите роль: комик или гость', reply_markup=kb_user_role)


@dp.message_handler(state=User.phone)
async def enter_phone(message: Message, state: FSMContext):
    await state.update_data({'phone': message.text})
    await message.answer(f'Введи свой e-mail:', reply_markup=kb_cancel)
    await User.next()


@dp.message_handler(state=User.email)
async def enter_email(message: Message, state: FSMContext):
    await state.update_data({'email': message.text})
    await message.answer(f'Введи свой город:', reply_markup=kb_cancel)
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
async def enter_confirm(message: Message, state: FSMContext):
    if message.text == 'Да':
        data = await state.get_data()
        user = {"tg_id": message.from_user.id, "name": data["name"],
                "role": data["role"], "phone": data["phone"],
                "email": data["email"], "city": data["city"]}
        db.new_user(user)
        await state.finish()
        await start_message(message)
    else:
        await state.reset_data()
        await start_message(message)


