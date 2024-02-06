from app.core.autho import login_get_token, get_current_user, oauth2_scheme
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from fastapi import APIRouter, Depends
from app.db.models.models import get_db
from sqlalchemy.orm import Session
from app.schemas.schemas import Token
from sqlalchemy.ext.asyncio import AsyncSession

token_router = APIRouter(tags=["token"])
@token_router.post("/token/", response_model=Token)
async def get_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: AsyncSession = Depends(get_db)):
    return await login_get_token(form_data=form_data, db=db)

@token_router.post("/me")
async def get_by_token(token: Annotated[str, Depends(oauth2_scheme)], db: AsyncSession = Depends(get_db)):
    return await get_current_user(token=token, db=db)