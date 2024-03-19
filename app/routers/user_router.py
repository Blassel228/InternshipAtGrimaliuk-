from app.schemas.schemas import User
from fastapi import APIRouter, Depends
from app.schemas.schemas import UserUpdateIn, UserUpdate
from app.utils.deps import get_current_user, get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.CRUD.user_crud import user_crud
from app.services.user_service import user_service

user_router = APIRouter(tags=["user"], prefix="/user")

@user_router.put("/self_update")
async def self_update(data: UserUpdateIn, current_user = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await user_service.self_update(id_=current_user.id,data=UserUpdate(**data.model_dump(), update_by=current_user.id), db=db)

@user_router.delete("/self_delete")
async def user_delete(current_user = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await user_service.delete(id_=current_user.id, db=db)
@user_router.put("/")
async def update(db: AsyncSession = Depends(get_db), data: User = None, id_: int = None):
    return await user_service.update(id_=id_, db=db, data=data)

@user_router.delete("/")
async def delete(db: AsyncSession = Depends(get_db), id_: int = None):
    return await user_service.delete(id_=id_, db=db)

@user_router.get("{id}")
async def get(id_: int = None, db: AsyncSession = Depends(get_db)):
    return await user_crud.get_one(id_=id_, db=db)

@user_router.post("/")
async def create(data: User, db: AsyncSession = Depends(get_db)):
    return await user_crud.add(data=data, db=db)
@user_router.get("/")
async def get_all(db: AsyncSession = Depends(get_db)):
    return await user_crud.get_all(db=db)