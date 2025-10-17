import sqlite3

def init_db(path_db) :
    with sqlite3.connect(path_db) as conn :
        cur = conn.cursor()
        cur.execute(""" CREATE TABLE if not exists users(id TEXT PRIMARY KEY, name TEXT , lastname TEXT , phone TEXT , email TEXT ,
                        password TEXT , membership_date TEXT , last_visit TEXT) """)
        conn.commit()
