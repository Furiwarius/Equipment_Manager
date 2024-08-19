import re
from pydantic import BaseModel, field_validator, EmailStr, Field


class NewUser(BaseModel):
    login: str = Field(..., min_length=8)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=64)
    timezone: str



class User(BaseModel):
    login: str = Field(..., min_length=8)
    password: str = Field(..., min_length=8, max_length=64)



class Code(BaseModel):
    code:int

    @field_validator("code")
    @classmethod
    def validate_email(cls, value):
        if value!=5:
            raise ValueError("Code is invalid")
        return value 


class NewFirm(BaseModel):
    name: str = Field(..., min_length=6, max_length=64)


class NewConstruction(BaseModel):
    name: str
    project: str
    address: str