from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from loader import dp


@dp.message_handler(Text(equals='Отмена'), state='*')
async def com_start(message: Message, state: FSMContext):
    await state.reset_state()
    await state.finish()
    await message.answer(text='Используйте /start для возврата в главное меню',
                         reply_markup=ReplyKeyboardRemove())