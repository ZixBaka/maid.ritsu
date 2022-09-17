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
    try:
        cursor.execute(f"""INSERT INTO cars VALUES(?,?,?,?,?)""", data)
    except sql.IntegrityError:
        cursor.execute(f"""UPDATE cars 
        SET number = ?, extra=?, extra2=?, contact=?""", data[1:])
    finally:
        base.commit()


async def check_user_db(id_code):
    base = sql.connect('user_data.db')
    cursor = base.cursor()
    cursor.execute(f"""SELECT ROWID FROM cars WHERE id = {id_code}""")
    return False if cursor.fetchone() is None else True


async def delete_user_db(id_code):
    base = sql.connect('user_data.db')
    cursor = base.cursor()
    cursor.execute(f"""DELETE FROM cars WHERE id = {id_code}""")
    base.commit()


async def user_info_db(id_code):
    base = sql.connect('user_data.db')
    cursor = base.cursor()
    cursor.execute(f"""SELECT * FROM cars WHERE id={id_code}""")
    x = cursor.fetchall()
    return x[0] if x != list() else None
