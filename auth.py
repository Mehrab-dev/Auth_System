import uuid
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
