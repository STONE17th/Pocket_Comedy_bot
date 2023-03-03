from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.middlewares import BaseMiddleware

from loader import dp, db


class UserStatus(BaseMiddleware):
    async def on_process_message(self, message: Message, data: dict):
        status = db.get_user_status(message.from_user.id)
        data['user_status'] = status[0] if status else status
