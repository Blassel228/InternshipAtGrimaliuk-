from pydantic import BaseModel, EmailStr, field_validator
from fastapi import HTTPException
from typing import Optional
from datetime import datetime

class User(BaseModel):
    id: int
    username: str
    password: str
    mail: EmailStr
    #registered_date: datetime
    role: int
    #hashed_password: str

class UserUpdateIn(BaseModel):
    username: str
    password: str
    email: Optional[EmailStr] = None

class UserUpdate(BaseModel):
    username: str
    password: str
    email: Optional[EmailStr] = None

    @field_validator("email")
    @classmethod
    def email_validator(cls, email):
        if email is not None:
            raise HTTPException(detail="Email cannot be changed", status_code=403)
        return email

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: int
    username: str