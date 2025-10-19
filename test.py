import sqlite3
from xml.dom.minidom import CDATASection

import auth
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

def test_delete_user(tmp_path) :
    fake_path = tmp_path / "data.sqlite3"
    user = User('Alex','Teles','09158435540','12345678',)
    pdb = auth.AuthUser(path_db=fake_path)
    pdb.Add_User(user)
    del_user = pdb.Delete_User(phone='09158435540')
    assert del_user  == True
