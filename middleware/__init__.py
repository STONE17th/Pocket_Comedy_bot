from aiogram import Dispatcher
from .status_mw import UserStatus


def setup(dp: Dispatcher):
    dp.middleware.setup(UserStatus())