from aiogram import Bot, Dispatcher
from os import getenv
from data_base import DataBase
from aiogram.contrib.fsm_storage.memory import MemoryStorage

memory = MemoryStorage()


bot = Bot(getenv('TOKEN'))
dp = Dispatcher(bot, storage=memory)
db = DataBase()
