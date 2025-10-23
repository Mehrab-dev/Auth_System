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
        time = datetime.datetime.today().strftime("%y-%m-%d  %H:%M:%S")
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
            old_data = cur.execute(""" SELECT name,lastname,email,password FROM users WHERE phone = ? """,(phone,))
            fetch_data = old_data.fetchall()
            if not fetch_data :
                logger.error("no users are registered in the database !")
                raise ValueError("no users are registered in the database !")
            else :
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
                if email is not None :
                    match = re.fullmatch(r"[a-zA-Z0-9_.]+@gmail\.com$", email)
                    if match :
                        new_email = email
                    else :
                        logger.error("email is invalid")
                        new_email = old_email
                else :
                    new_email = old_email
                if password is not None :
                    new_password = bcrypt.hashpw(password.encode(),bcrypt.gensalt())
                else :
                    new_password = old_password
            try :
                cur.execute(""" UPDATE users SET name = ? ,lastname = ? ,email = ? ,password = ? WHERE phone = ?""",
                            (new_name,new_lastname,new_email,new_password,phone))
                conn.commit()
                logger.info("User information updated")
                return True
            except Exception as e :
                logger.error(f"error connection to database : {e}")
                raise ValueError("error connection to database")

    def login_user(self,phone:str,password:str) :
        time = datetime.datetime.now().strftime("%y-%m-%d  %H:%M:%S")
        try :
            with sqlite3.connect(self.path_db) as conn :
                cur = conn.cursor()
                exists = cur.execute(""" SELECT password FROM users WHERE phone = ? """, (phone,))
                data = exists.fetchall()
                if not data :
                    logger.error("no user has been registered with this mobile number")
                    return False
                for i in data :
                    old_password = i[0]
                if bcrypt.checkpw(password.encode(),str(old_password).encode()) :
                    cur.execute(""" UPDATE users SET last_visit = ? WHERE phone = ? """,(time,phone))
                    conn.commit()
                    logger.info("your login has been confirmed")
                    return  True
                else :
                    logger.warning("password is invalid")
                    return False
        except Exception as e :
            logger.error(f"error connection to database! : {e} ")
            return False



