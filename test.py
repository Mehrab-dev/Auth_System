import sqlite3
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

def test_update_user(tmp_path) :
    fake_path = tmp_path / "data.sqlite3"
    user = User("Alex","Teles","09308342034","12341234")
    pdb = AuthUser(fake_path)
    pdb.Add_User(user)
    u_user = pdb.Update_User("09308342034","Dani")
    assert u_user == True

def test_login_user(tmp_path) :
    fake_path = tmp_path / "data.sqlite3"
    pdb = AuthUser(path_db=fake_path)
    user = User("Hadi","Mohammadi","09158494050","12345678")
    pdb.Add_User(user)
    login_user = pdb.login_user("09158494050","12345678")
    assert login_user == True