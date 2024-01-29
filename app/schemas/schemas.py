from pydantic import BaseModel, EmailStr
import datetime
from typing import List

class User(BaseModel):
    id: int
    username: str
    password: str
    mail: EmailStr
    #registered_date: datetime.datetime
    role: int
    #hashed_password: str

class UserUpdate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: int
    username: str