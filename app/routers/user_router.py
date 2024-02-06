from typing import Annotated
from fastapi import APIRouter, Depends
from app.db.models.models import get_db
from app.schemas.schemas import UserUpdateIn, UserUpdate
from app.services.user_service import user_service
from app.core.autho import oauth2_scheme, get_current_user
from sqlalchemy.ext.asyncio import AsyncSession

user_router = APIRouter(tags=["user"])

@user_router.put("/update")
async def user_update(data: UserUpdateIn, current_user = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await user_service.update(data=UserUpdate(**data.model_dump(), update_by=current_user.id), db=db)

@user_router.delete("/self_delete")
async def user_delete(current_user = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await user_service.delete(id_=current_user.id, db=db)
