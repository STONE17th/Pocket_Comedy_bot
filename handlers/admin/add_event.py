from loader import dp, db
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from states import Event
from handlers.start import start_message
from keyboards.standart import kb_yes_no, kb_city_select, kb_cancel, create_kb_loca_select


@dp.message_handler(commands=['add_event', 'новая_туса'], state=None)
async def add_new_event(message: Message, user_status: str):
    if user_status == 'Admin':
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
async def enter_description(message: Message, state: FSMContext):
    if message.text != 'Нет':
        await state.update_data({'description': message.text})
    await message.answer(f'В каком городе состоится мероприятие (выбери или напиши свой):',
                         reply_markup=kb_city_select)
    await Event.city_loca.set()


@dp.message_handler(state=Event.city_loca)
async def enter_city_loca(message: Message, state: FSMContext):
    await state.update_data({'city_loca': message.text})
    await message.answer(f'Выбери площадку из списка или создай новую:',
                         reply_markup=create_kb_loca_select(message.text))
    await Event.name_loca.set()


@dp.message_handler(state=Event.name_loca)
async def enter_name_loca(message: Message, state: FSMContext):
    await state.update_data({'name_loca': message.text})
    data = await state.get_data()
    city = data["city_loca"]
    locations = db.all_locations(city)
    find = False
    for loca in locations:
        if message.text == loca[0]:
            find = True
            break
    if find:
        await message.answer(f'Введите дату мероприятия:')
        await Event.date.set()
    else:
        await message.answer(f'Такой площадки нет в нашей БД. Давайте ее зарегистрируем...\n'
                             f'Адрес площадки:', reply_markup=kb_cancel)
        await Event.address_loca.set()


@dp.message_handler(state=Event.address_loca)
async def enter_address_loca(message: Message, state: FSMContext):
    await state.update_data({'address_loca': message.text})
    await message.answer(f'Телефон площадки:', reply_markup=kb_cancel)
    await Event.phone_loca.set()


@dp.message_handler(state=Event.phone_loca)
async def enter_phone_loca(message: Message, state: FSMContext):
    await state.update_data({'phone_loca': message.text})
    await message.answer(f'Адрес в Интернет: ', reply_markup=kb_cancel)
    await Event.url_loca.set()


@dp.message_handler(state=Event.url_loca)
async def enter_url_loca(message: Message, state: FSMContext):
    await state.update_data({'url_loca': message.text})
    data = await state.get_data()
    message_text = f'Название: {data["name_loca"]}\nГород: {data["city_loca"]}\n' \
                   f'Адрес: {data["address_loca"]}\nТелефон: {data["phone_loca"]}\n' \
                   f'Интернет: {data["url_loca"]}\n\nДанные введены верно?'
    await message.answer(message_text, reply_markup=kb_yes_no)
    await Event.confirm_loca.set()


@dp.message_handler(state=Event.confirm_loca)
async def enter_confirm_loca(message: Message, state: FSMContext):
    if message.text in ['Да', 'Нет']:
        if message.text == 'Да':
            data = await state.get_data()
            location = {"city": data["city_loca"], "name": data["name_loca"],
                        "address": data["address_loca"], "phone": data["phone_loca"],
                        "url": data["url_loca"]}
            db.new_location(location)
            await message.answer(f'Площадка добавлена в нашу БД\nВведите дату мероприятия:')
            await Event.date.set()
        else:
            await enter_description(message, state)
    else:
        await enter_url_loca(message, state)


@dp.message_handler(state=Event.date)
async def enter_date(message: Message, state: FSMContext):
    await state.update_data({'date': message.text})
    await message.answer(f'Цена входного билета: ', reply_markup=kb_cancel)
    await Event.price.set()


@dp.message_handler(state=Event.price)
async def enter_url(message: Message, state: FSMContext):
    if message.text != 'Нет':
        await state.update_data({'price': message.text})
    data = await state.get_data()
    message_text = f'Название: {data["name"]}\nОписание: {data["description"]}\n' \
                   f'Площадка: {data["name_loca"]} ({data["city_loca"]})\n' \
                   f'Дата: {data["date"]}\nЦена: {data["price"]}\n\nДанные введены верно?'
    await dp.bot.send_photo(message.from_user.id, photo=data['poster'], caption=message_text, reply_markup=kb_yes_no)
    await Event.confirm.set()


@dp.message_handler(state=Event.confirm)
async def enter_confirm(message: Message, user_status, state: FSMContext):
    if message.text in ['Да', 'Нет']:
        if message.text == 'Да':
            data = await state.get_data()
            city_loca = data["city_loca"]
            name_loca = data["name_loca"]
            id_loca = db.get_id_loca(city=city_loca, name=name_loca)[0]
            event = {"name": data["name"], "poster": data["poster"],
                     "description": data["description"],
                     "location_id": id_loca, "user_id": message.from_user.id,
                     "date": data["date"], "price": data["price"]}
            db.new_event(event)
            await state.finish()
            await start_message(message, user_status)

        else:
            await state.reset_data()
            await add_new_event(message, user_status)
    else:
        await enter_url(message, state)
