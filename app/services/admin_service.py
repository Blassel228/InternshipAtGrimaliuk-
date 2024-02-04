from app.schemas.schemas import User#, UserIn
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.admin_repo import admin_repo
from fastapi import HTTPException
class AdminService:
    async def get_all(self, db: AsyncSession):
        return await admin_repo.get_all(db=db)

    async def get_one(self, id_: int, db: AsyncSession):
        return await admin_repo.get_one(id_=id_, db=db)

    async def add(self, data: User, db:AsyncSession):
        user = await admin_repo.add(data=data, db=db)
        if user is None:
            raise HTTPException(status_code=404, detail="Idi nahui")
        return user
    async def update(self, id_: int, data: User, db: Session):
        user = await admin_repo.update(id_=id_, data=data, db=db)
        if user is None:
            raise HTTPException(status_code=404, detail="The user is not valid")
        return user

    async def delete(self, id_: int, db: Session):
        user = await admin_repo.delete(id_=id_, db=db)
        if user is None:
            raise HTTPException(status_code=404, detail="The user is not valid")
        return user

admin_service = AdminService()