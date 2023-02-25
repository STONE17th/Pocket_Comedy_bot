from loader import dp, db
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from states import Location, Event
from handlers.start import start_message
from handlers.admin.add_loacation import add_new_location
from keyboards.standart import kb_yes_no, kb_loca_select, kb_cancel


@dp.message_handler(commands=['add_event', 'новая_туса'], state=None)
async def add_new_event(message: Message):
    user_role = db.get_user_role(message.from_user.id)
    print('Готов добавлять')
    if user_role and user_role[0] == 'Админ':
        await message.answer(f'Приветствую, {message.from_user.first_name}!\n'
                             f'Давай создадим новое мероприятие в нашей БД\n'
                             f'Введи название мероприятия: ', reply_markup=kb_cancel)
        await Event.name.set()
    else:
        await message.answer(f'Извините, для Вас эта команда не доступна')


@dp.message_handler(state=Event.name)
async def enter_name(message: Message, state: FSMContext):
    await state.update_data({'name': message.text})
    await message.answer(f'Загрузи афишу мероприятия (формат 300*200):', reply_markup=kb_cancel)
    await Event.next()


@dp.message_handler(content_types='photo', state=Event.poster)
async def enter_city(message: Message, state: FSMContext):
    await state.update_data({'poster': message.photo[0].file_id})
    await message.answer(f'Введи описание мероприятия:', reply_markup=kb_cancel)
    await Event.next()


@dp.message_handler(state=Event.description)
async def enter_address(message: Message, state: FSMContext):
    await state.update_data({'description': message.text})
    await message.answer(f'Место проведения мероприятия (выбери или создай новое):',
                         reply_markup=kb_loca_select)
    await Event.next()


@dp.message_handler(state=Event.location)
async def enter_phone(message: Message, state: FSMContext):
    find_loca = True
    for loca, city in set(db.all_locations()):
        if message.text == f'{loca} ({city})':
            await state.update_data({'location': message.text})
            await message.answer(f'Дата мероприятия: ', reply_markup=kb_cancel)
            find_loca = False
            await Event.next()
    if find_loca:
        await message.answer('Такой площадки нет в нашей базе, давайте ее создадим...')
        await add_new_location(message, state, True)


@dp.message_handler(state=Event.date)
async def enter_phone(message: Message, state: FSMContext):
    await state.update_data({'date': message.text})
    await message.answer(f'Цена входного билета: ', reply_markup=kb_cancel)
    await Event.next()


@dp.message_handler(state=Event.price)
async def enter_url(message: Message, state: FSMContext):
    await state.update_data({'price': message.text})
    data = await state.get_data()
    message_text = f'Название: {data["name"]}\nОписание: {data["description"]}\nПлощадка: {data["location"]}\n' \
                   f'Дата: {data["date"]}\nЦена: {data["price"]}\n\nДанные введены верно?'
    await dp.bot.send_photo(message.from_user.id, photo=data['poster'], caption=message_text, reply_markup=kb_yes_no)
    await Event.next()


@dp.message_handler(state=Event.confirm)
async def enter_confirm(message: Message, state: FSMContext):
    if message.text == 'Да':
        data = await state.get_data()
        event = {"name": data["name"], "poster": data["poster"],
                 "description": data["description"],
                 "location": data["location"], "date": data["date"],
                 "price": data["price"]}
        db.new_location(event)
        await state.finish()
        await start_message(message)

    else:
        await state.reset_data()
        await add_new_event(message)
