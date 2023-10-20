from db.models.models import UserModel
from sqlalchemy.orm import Session
from schemas.schemas import User, UserListResponse
from fastapi import HTTPException
from passlib.context import CryptContext
import logging

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_all_users(db: Session):
    return db.query(UserListResponse).all()

def get_user(id_: int, db: Session):
    return db.query(UserModel).filter(UserModel.id==id_).first()

def create_user(data: User, db: Session):
    #explanation for you from the future: we pass a password to our API it takes it and transforms to hash then it saves the password to the database
    user = UserModel(id=data.id, username=data.username, mail=data.mail, role=data.role, hashed_password=pwd_context.hash(data.password))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except Exception as ex:
        logging.error("User was not created")
        return ex
    return user

def update_user(data: User, id_: int, db: Session):
    try:
        user = db.query(UserModel).filter(UserModel.id==id_).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user.id = data.id
        user.username = data.username
        user.password = data.password
        user.hashed_password = pwd_context.hash(data.password)
        user.mail = data.mail

        db.commit()
        db.refresh(user)
    except Exception as ex:
        logging.error("User was not updated")
        return ex

    logging.info("User was updated")
    return user

def delete_user(id_: int, db: Session):
    try:
        user = db.query(UserModel).filter(UserModel.id==id_).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        db.delete(user)
        db.commit()
        db.refresh(user)
    except Exception as ex:
        logging.error("User could not be deleted")
        return ex

    return f"{user} was deleted"