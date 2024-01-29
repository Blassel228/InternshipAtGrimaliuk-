from datetime import timedelta, datetime
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from fastapi import  Depends, status, HTTPException
from passlib.context import CryptContext
from app.db.models.models import get_db, UserModel
from jose import jwt, JWTError
from config import settings
from sqlalchemy import select
from sqlalchemy.orm import Session


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token/")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def login_get_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user = authenticate_user(username=form_data.username, password=form_data.password, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=20)
    access_token = create_access_token(
        data={"username": user.username, "id": user.id},
        expires_delta=access_token_expires
    )
    #acrually it will return {"username":  "zero","id": 443, "exp": 1705839660}
    return {"access_token": access_token, "token_type": "bearer"}

def authenticate_user(password: str, username: str, db: Session = Depends(get_db)):
    user = db.execute(select(UserModel).where(UserModel.username == username)).scalar()
    if not user:
        return False
    if not pwd_context.verify(password ,user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret, algorithm=settings.algorithm)
    return encoded_jwt

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],db: Session):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, settings.secret, algorithms=[settings.algorithm])
        user_id: int = payload.get("id")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.execute(select(UserModel).where(UserModel.id==user_id)).scalar()
    if user is None:
        raise credentials_exception
    return user