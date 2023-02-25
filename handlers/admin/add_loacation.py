from loader import dp, db
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from states import Location, Event
from handlers.start import start_message
from keyboards.standart import kb_yes_no, kb_city_select, kb_cancel


@dp.message_handler(commands=['add_loca', 'новая_лока'], state=[None, Event.location])
async def add_new_location(message: Message, state: FSMContext, option: bool = False):
    user_role = db.get_user_role(message.from_user.id)
    if user_role and user_role[0] == 'Админ':
        await message.answer(f'Приветствую, {message.from_user.first_name}!\n'
                             f'Давай создадим новую локацию в нашей БД\n'
                             f'Введи название площадки', reply_markup=kb_cancel)
        await state.update_data({'option': option})
        await Location.name.set()
    else:
        await message.answer(f'Извините, для Вас эта команда не доступна')


@dp.message_handler(state=Location.name)
async def enter_name(message: Message, state: FSMContext):
    print(state)
    await state.update_data({'name': message.text})
    await message.answer(f'Выбери город из списка или введи новый:', reply_markup=kb_city_select)
    await Location.next()


@dp.message_handler(state=Location.city)
async def enter_city(message: Message, state: FSMContext):
    await state.update_data({'city': message.text})
    await message.answer(f'Адрес площадки:', reply_markup=kb_cancel)
    await Location.next()


@dp.message_handler(state=Location.address)
async def enter_address(message: Message, state: FSMContext):
    await state.update_data({'address': message.text})
    await message.answer(f'Телефон площадки:', reply_markup=kb_cancel)
    await Location.next()


@dp.message_handler(state=Location.phone)
async def enter_phone(message: Message, state: FSMContext):
    await state.update_data({'phone': message.text})
    await message.answer(f'Адрес в Интернет: ', reply_markup=kb_cancel)
    await Location.next()


@dp.message_handler(state=Location.url)
async def enter_url(message: Message, state: FSMContext):
    await state.update_data({'url': message.text})
    data = await state.get_data()
    message_text = f'Название: {data["name"]}\nГород: {data["city"]}\nАдрес: {data["address"]}\n' \
                   f'Телефон: {data["phone"]}\nИнтернет: {data["url"]}\n\nДанные введены верно?'
    await message.answer(message_text, reply_markup=kb_yes_no)
    await Location.next()


@dp.message_handler(state=Location.confirm)
async def enter_confirm(message: Message, state: FSMContext):
    if message.text == 'Да':
        data = await state.get_data()
        location = {"name": data["name"], "city": data["city"], "address": data["address"],
                    "phone": data["phone"], "url": data["url"]}
        db.new_location(location)
        if data["option"]:
            await message.answer(f'{data["name"]} ({data["city"]})')
            await Event.date.set()
        else:
            await state.finish()
            await start_message(message)
    else:
        await state.reset_data()
        await add_new_location(message)


