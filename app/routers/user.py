from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.db.models.models import get_db
from sqlalchemy.orm import Session
from app.schemas.schemas import User
from app.services.user import user_service
from app.core.autho import login_get_token, get_current_user, oauth2_scheme

user_router = APIRouter(tags=["user"])

@user_router.put("/")
async def update(db: Session = Depends(get_db), data: User = None, id_: int = None):
    return user_service.update_user(id_=id_, db=db, data=data)

@user_router.delete("/")
def delete(db: Session = Depends(get_db), id_: int = None):
    return user_service.delete_user(id_=id_, db=db)

@user_router.get("{id}")
async def get(id_: int = None, db: Session = Depends(get_db)):
    return user_service.get_one(id_=id_, db=db)

@user_router.post("/")
async def create(db: Session = Depends(get_db), data: User = None):
    return user_service.add_user(db=db, data=data)
@user_router.get("/")
async def get_all(db: Session = Depends(get_db)):
    return user_service.get_all(db=db)

@user_router.post("/token")
def get_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return login_get_token(db=db, form_data=form_data, token=token)

@user_router.post("/me")
def get_by_token():
    get_current_user()