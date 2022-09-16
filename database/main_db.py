import sqlite3 as sql


async def db_start():
    base = sql.connect('user_data.db')
    if base:
        print('Data base activated')
    base.execute('''CREATE TABLE IF NOT EXISTS cars(
    id TEXT PRIMARY KEY,
    number TEXT,
    extra TEXT,
    extra2 TEXT,
    contact TEXT
    )''')


async def insert_new_db(*data):
    base = sql.connect('user_data.db')
    cursor = base.cursor()
    cursor.execute(f"""INSERT INTO cars VALUES(?,?,?,?,?)""", data)
    base.commit()


async def check_user_db(id_code):
    base = sql.connect('user_data.db')
    cursor = base.cursor()
    cursor.execute(f"""SELECT ROWID FROM cars WHERE id = {id_code}""")
    return False if cursor.fetchone() is None else True




