from typing import Annotated
from fastapi import APIRouter, Depends
from app.db.models.models import get_db
from sqlalchemy.orm import Session
from app.schemas.schemas import UserUpdate
from app.services.user_service import user_service
from app.core.autho import oauth2_scheme
from sqlalchemy.ext.asyncio import AsyncSession

user_router = APIRouter(tags=["user"])

@user_router.put("/self_update")
async def user_self_update(token: Annotated[str, Depends(oauth2_scheme)], db: AsyncSession = Depends(get_db), data: UserUpdate = None):
    return await user_service.update(token=token, data=data, db=db)

@user_router.delete("/self_delete")
async def user_self_delete(token: Annotated[str, Depends(oauth2_scheme)], db: AsyncSession = Depends(get_db)):
    return await user_service.delete(token=token, db=db)
