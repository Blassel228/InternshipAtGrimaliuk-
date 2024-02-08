from typing import Optional
from datetime import datetime
from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, model_validator


class User(BaseModel):
    id: int
    username: str
    password: str
    mail: EmailStr
    role: int

class UserUpdateIn(BaseModel):
    id: int
    username: Optional[str] = None
    password: Optional[str] = None
    mail: Optional[EmailStr] = None

class UserUpdate(BaseModel):
    id: int
    username: Optional[str] = None
    password: Optional[str] = None
    mail: Optional[EmailStr] = None
    update_by: int

    @model_validator(mode="after")
    def validator(cls, values):
        if values.update_by != values.id:
            raise HTTPException(detail="User can change only itself", status_code=403)
        if values.mail is not None:
            raise HTTPException(detail="Email cannot be changed", status_code=403)
        return values.mail

class Token(BaseModel):
    access_token: str
    token_type: str

class CompanySchemaIn(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    visible: Optional[bool] = True
class CompanySchema(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    visible: Optional[bool] = True
    owner_id: int

