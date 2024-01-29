from app.core.autho import login_get_token, get_current_user, oauth2_scheme
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from fastapi import APIRouter, Depends
from app.db.models.models import get_db
from sqlalchemy.orm import Session
from app.schemas.schemas import Token

token_router = APIRouter(tags=["token"])
@token_router.post("/token/", response_model=Token)
def get_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    return login_get_token(db=db, form_data=form_data)

@token_router.post("/me")
def get_by_token(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    return get_current_user(token, db)
