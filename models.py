import re
import bcrypt


class User :
    def __init__(self,name:str,lastname:str,phone:str,password:str,email:str=None) :
        self.name = name
        self.lastname = lastname
        match = re.fullmatch(r"\d{11}",phone)
        if not match :
            raise ValueError("The phone number is invalid")
        else :
            self.phone = phone
        self.password = bcrypt.hashpw(password.encode(),bcrypt.gensalt())
        if email is not None :
            match = re.fullmatch(r"^[a-zA-Z0-9._]+@gmail\.com$",email)
            if not match :
                raise ValueError("The email is invalid")
            else :
                self.email = email
        else :
            self.email = None

