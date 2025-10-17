import sqlite3


from models import User
from auth import AuthUser

def test_adduser(tmp_path) :
    fake_data = tmp_path / 'data.sqlite3'
    user = User('Alex','Teles','09126592016','12345678')
    pdb = AuthUser(path_db=fake_data)
    pdb.Add_User(user)
    with sqlite3.connect(fake_data) as conn :
        cur = conn.cursor()
        data = cur.execute(""" SELECT name,phone from users """)
        for i in data :
            name , phone = i
    assert name == "Alex"
    assert phone == '09126592016'