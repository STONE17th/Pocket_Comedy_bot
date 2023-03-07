import sqlite3


class DataBase:

    def __init__(self, db_path: str = 'data_base/pc_db.db'):
        self.db_path = db_path

    @property
    def connection(self):
        return sqlite3.connect(self.db_path)

    def execute(self, sql: str, parameters: tuple = tuple(),
                fetchone=False, fetchall=False, commit=False):
        connection = self.connection
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)
        if commit:
            connection.commit()
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()
        connection.close()
        return data


    def create_table_users(self):
        sql = '''CREATE TABLE IF NOT EXISTS users 
        (user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        tg_id INTEGER, name VARCHAR, role VARCHAR, phone VARCHAR, 
        email VARCHAR, city VARCHAR, premium VARCHAR)'''
        self.execute(sql, commit=True)

    def create_table_events(self):
        sql = '''CREATE TABLE IF NOT EXISTS events 
        (event_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR, photo VARCHAR, description VARCHAR,
        location_id INTEGER, user_id INTEGER, date VARCHAR,
        price REAL)'''
        self.execute(sql, commit=True)

    def create_table_locations(self):
        sql = '''CREATE TABLE IF NOT EXISTS locations 
        (location_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR, city VARCHAR, address VARCHAR,
        phone VARCHAR, url VARCHAR)'''
        self.execute(sql, commit=True)

    def create_table_comic_events(self):
        sql = '''CREATE TABLE IF NOT EXISTS comic_events 
        (event_id INTEGER, user_id INTEGER, CONSTRAINT users_PK PRIMARY KEY (event_id, user_id))'''
        self.execute(sql, commit=True)

    def create_table_guest_events(self):
        sql = '''CREATE TABLE IF NOT EXISTS guest_events 
        (event_id INTEGER, user_id INTEGER, CONSTRAINT users_PK PRIMARY KEY (event_id, user_id))'''
        self.execute(sql, commit=True)

    def new_user(self, user: dict):
        parameters = (user.get('tg_id'), user.get('name'), user.get('role'), user.get('phone'),
                      user.get('email'), user.get('city'), False)
        sql = '''INSERT INTO users (tg_id, name, role, phone, email, city, premium) 
                VALUES (?, ?, ?, ?, ?, ?, ?)'''
        self.execute(sql, parameters, commit=True)


    def get_user_status(self, tg_id: int):
        parameters = (tg_id,)
        sql = '''SELECT role FROM users WHERE tg_id=?'''
        return self.execute(sql, parameters, fetchone=True)



    def new_event(self, event: dict):
        parameters = (event.get('name'), event.get('poster'), event.get('description'), event.get('location_id'),
                      event.get('user_id'), event.get('date'), event.get('price'))
        sql = '''INSERT INTO events (name, photo, description, location_id, user_id, date, price) 
                VALUES (?, ?, ?, ?, ?, ?, ?)'''
        self.execute(sql, parameters, commit=True)

    def new_location(self, user: dict):
        parameters = (user.get('name'), user.get('city'), user.get('address'),
                      user.get('phone'), user.get('url'))
        sql = '''INSERT INTO locations (name, city, address, phone, url) 
                VALUES (?, ?, ?, ?, ?)'''
        self.execute(sql, parameters, commit=True)

    def all_cities(self):
        sql = '''SELECT DISTINCT city FROM locations'''
        return self.execute(sql, fetchall=True)

    def get_city_by_id(self, location_id):
        parameters = (location_id,)
        sql = '''SELECT city FROM locations WHERE location_id=?'''
        return self.execute(sql, parameters, fetchone=True)
    def all_locations(self, city: str):
        parameters = (city,)
        sql = '''SELECT DISTINCT name FROM locations WHERE city=?'''
        return self.execute(sql, parameters, fetchall=True)

    def all_events(self):
        sql = '''SELECT * FROM events'''
        return self.execute(sql, fetchall=True)

    def all_dates(self):
        sql = '''SELECT DISTINCT date FROM events'''
        return self.execute(sql, fetchall=True)

    def all_orgs(self):
        sql = '''SELECT DISTINCT user_id FROM events'''
        return self.execute(sql, fetchall=True)

    def get_location_id(self, **kwargs):
        sql = '''SELECT location_id FROM locations WHERE '''
        sql, parameters = self.extract_kwargs(sql, kwargs)
        return self.execute(sql, parameters, fetchone=True)

    def get_location(self, location_id: int):
        parameters = (location_id,)
        sql = '''SELECT * FROM locations WHERE location_id=?'''
        return self.execute(sql, parameters, fetchall=True)

    def get_name_and_city_location(self, location_id: int):
        parameters = (location_id,)
        sql = '''SELECT name, city FROM locations WHERE location_id=?'''
        return self.execute(sql, parameters, fetchall=True)

    def get_all_events_in_location(self, location_id: int):
        parameters = (location_id,)
        sql = '''SELECT * FROM events WHERE location_id=?'''
        return self.execute(sql, parameters, fetchall=True)

    def get_all_events_by(self, **kwargs):
        sql = '''SELECT * FROM events WHERE '''
        sql, parameters = self.extract_kwargs(sql, kwargs)
        return self.execute(sql, parameters, fetchall=True)


    def city_locations(self, city: str):
        parameters = (city,)
        sql = '''SELECT locations.name FROM locations Where city=?'''
        return self.execute(sql, parameters, fetchall=True)


    def get_user_name(self, user_id: int):
        parameters = (user_id,)
        sql = '''SELECT name FROM users WHERE tg_id=?'''
        return self.execute(sql, parameters, fetchone=True)


    def user_events(self, tg_id):
        parameters = (tg_id,)
        sql = '''SELECT event_id FROM comic_events Where user_id=?'''
        return self.execute(sql, parameters, fetchall=True)




    # def create_table_basket(self):
    #     sql = '''CREATE TABLE IF NOT EXISTS basket
    #     (id_order INTEGER PRIMARY KEY AUTOINCREMENT,
    #     id_user INTEGER, id_goods INTEGER)'''
    #     self.execute(sql, commit=True)
    #
    # def create_table_purchase(self):
    #     sql = '''CREATE TABLE IF NOT EXISTS purchase
    #     (id_order INTEGER PRIMARY KEY AUTOINCREMENT,
    #     name TEXT, phone_number TEXT, email TEXT,
    #     shipping TEXT, address TEXT, goods TEXT)'''
    #     self.execute(sql, commit=True)
    #
    # def add_goods(self, goods: dict):
    #     parameters = (goods.get('g_type'), goods.get('image'), goods.get('name'),
    #                   goods.get('desc'), goods.get('quantity'), goods.get('price'))
    #     sql = '''INSERT INTO goods (g_type, image, name, desc, quantity, price)
    #     VALUES (?, ?, ?, ?, ?, ?)'''
    #     self.execute(sql, parameters, commit=True)
    #
    # def get_goods(self, **kwargs):
    #     sql = '''SELECT * FROM goods WHERE '''
    #     sql, parameters = self.extract_kwargs(sql, kwargs)
    #     return self.execute(sql, parameters, fetchall=True)
    #
    # def get_basket(self, **kwargs):
    #     sql = '''SELECT * FROM basket WHERE '''
    #     sql, parameters = self.extract_kwargs(sql, kwargs)
    #     return self.execute(sql, parameters, fetchall=True)
    #
    # def add_to_basket(self, id_user: int, id_goods: int):
    #     parameters = (id_user, id_goods)
    #     sql = '''INSERT INTO basket (id_user, id_good) VALUES (?, ?)'''
    #     self.execute(sql, parameters, commit=True)
    #     parameters = (id_goods,)
    #     sql = '''UPDATE goods SET quantity = quantity - 1 WHERE id=?'''
    #     self.execute(sql, parameters, commit=True)
    #
    # def remove_from_basket(self, id_order: int, id_goods: int):
    #     parameters = (id_order,)
    #     sql = '''DELETE FROM basket WHERE id_order=?'''
    #     self.execute(sql, parameters, commit=True)
    #     parameters = (id_goods,)
    #     sql = '''UPDATE goods SET quantity = quantity + 1 WHERE id=?'''
    #     self.execute(sql, parameters, commit=True)
    #
    # def clear_basket(self, id_user):
    #     parameters = (id_user,)
    #     sql = '''DELETE FROM basket WHERE id_user=?'''
    #     self.execute(sql, parameters, commit=True)
    #
    # def add_purchase(self, id_user: int, order: dict, shipping: str):
    #     sql = '''INSERT INTO purchase (name, phone_number, email, shipping, address, goods)
    #     VALUES (?, ?, ?, ?, ?, ?)'''
    #     for goods in self.get_basket(id_user=id_user):
    #         item = self.get_goods(id=int(goods[2]))
    #         parameters = (order.get('name'), order.get('phone_number'), order.get('email'),
    #                       shipping, str(order.get('shipping_address')), str(item[0][3]))
    #         self.execute(sql, parameters, commit=True)

    @staticmethod
    def extract_kwargs(sql: str, parameters: dict) -> tuple:
        sql += ' AND '.join([f'{key} = ?' for key in parameters])
        return sql, tuple(parameters.values())


    def disconnect(self):
        self.connection.close()