from fastapi import APIRouter, Depends
from app.schemas.schemas import UserUpdateIn, UserUpdate
from app.services.user_service import user_service
from app.utils.deps import get_current_user, get_db
from sqlalchemy.ext.asyncio import AsyncSession

user_router = APIRouter(tags=["user"], prefix="/user")

@user_router.put("/update")
async def user_update(data: UserUpdateIn, current_user = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await user_service.update(data=UserUpdate(**data.model_dump(), update_by=current_user.id), db=db)

@user_router.delete("/self_delete")
async def user_delete(current_user = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await user_service.delete(user_id=current_user.id, db=db)


