import re
import uuid

import bcrypt

from models import User
import sqlite3
import datetime
from logger_config import logger
from db import init_db

class AuthUser :
    def __init__(self,path_db) :
        self.path_db = path_db
        init_db(self.path_db)

    def Add_User(self,user:User) :
        user_id = str(uuid.uuid4())
        time = datetime.datetime.today()
        try :
            with sqlite3.connect(self.path_db) as conn :
                cur = conn.cursor()
                cur.execute(""" INSERT INTO users(id,name,lastname,phone,email,password,membership_date,last_visit) 
                                    VALUES(?,?,?,?,?,?,?,?) """,(user_id,user.name,user.lastname,user.phone,user.email,
                                    user.password,time,time))
                conn.commit()
            logger.info("User added successfully")
        except Exception as e :
            logger.error(f' error connecting to database : {e}')

    def Delete_User(self,phone) :
        try :
            with sqlite3.connect(self.path_db) as conn :
                cur = conn.cursor()
                exists = cur.execute(""" SELECT phone FROM users WHERE phone = ? """,(phone,))
                data = exists.fetchall()
                if not data :
                    logger.info("No user found with this mobile number")
                    return False
                cur.execute(""" DELETE FROM users WHERE phone = ? """,(phone,))
                conn.commit()
                if cur.rowcount > 0 :
                    logger.info("User deleted successfully")
                    return True
                else :
                    logger.info("User not deleted - not found")
                    return False
        except Exception as e :
            logger.error(f"error connecting to database : {e}")
            return False

    def Update_User(self,phone:str,name:str=None,lastname:str=None,password:str=None,email:str=None) :
        with sqlite3.connect(self.path_db) as conn :
            cur = conn.cursor()
            old_data = cur.execute(""" SELECT name,lastname,phone,email,password FROM users WHERE phone = ? """,(phone,))
            fetch_data = old_data.fetchall()
            for i in fetch_data :
                old_name,old_lastname,old_email,old_password = i
            if name is not None :
                new_name = name
            else :
                new_name = old_name
            if lastname is not None :
                new_lastname = lastname
            else :
                new_lastname = old_lastname
            match = re.fullmatch(r"\d[a-zA-Z0-9_.]+@gmail\.com$",(email,))
            if email is not None :
                if match :
                    new_email = email
                else :
                    logger.error("email is invalid")
            else :
                new_email = old_email
            if password is not None :
                bcrypt.hashpw(password.encode(),bcrypt.gensalt())
            else :
                new_password = old_password



