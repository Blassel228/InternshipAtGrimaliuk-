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

class UserSignIn(BaseModel):
    username: str
    password: str

class UserSignUp(BaseModel):
    username: str
    password: str
    mail: EmailStr

class UserListResponse(BaseModel):
    users: List[User]