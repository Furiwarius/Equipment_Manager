import re
from pydantic import BaseModel, field_validator


class NewUser(BaseModel):
    login: str
    email: str
    password: str


    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        if not bool(re.fullmatch(r'[\w.-]+@[\w-]+\.[\w.]+', value)):
            raise ValueError("Email is invalid")
        return value 


    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        password_length = len(value)
        if password_length < 8 or password_length > 16:
            raise ValueError("The password must be between 8 and 16 characters long")
        return value



class User(BaseModel):
    login:str
    password:str



class Code(BaseModel):
    code:int

    @field_validator("code")
    @classmethod
    def validate_email(cls, value):
        if value!=5:
            raise ValueError("Code is invalid")
        return value 