from aiogram import executor
from handlers import dp
from loader import db
import middleware

async def on_start(_):
    print('Бот запущен')
    try:
        db.create_table_users()
        db.create_table_locations()
        db.create_table_events()
        db.create_table_comic_events()
        db.create_table_guest_events()
        print('DB connected... OK!')
    except:
        print('DB failure!')

if __name__ == '__main__':
    middleware.setup(dp)
    executor.start_polling(dp, skip_updates=True, on_startup=on_start)




