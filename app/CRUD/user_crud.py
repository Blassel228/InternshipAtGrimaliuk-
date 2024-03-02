from app.db.models.models import UserModel
from passlib.context import CryptContext
from sqlalchemy import update, select, insert
from app.repositories.repository import CrudRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.schemas import User
from app.schemas.schemas import UserUpdate
from fastapi import HTTPException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserCrud(CrudRepository):
    async def update(self, id_: int, db: AsyncSession, data: User):
        data = data.model_dump()
        stmt = (update(self.model).values(hashed_password=pwd_context.hash(data.pop("password")),**data).
                where(self.model.id == id_))
        res = await db.execute(stmt)
        if res.rowcount==0:
            return None
        await db.commit()
        return data

    async def add(self, db: AsyncSession, data: User):
        data = data.model_dump()
        stmt = insert(self.model).values(hashed_password=pwd_context.hash(data.pop("password")), **data)
        res = await db.execute(stmt)
        if res.rowcount == 0:
            return None
        await db.commit()
        res = await db.scalars(select(self.model).where(self.model.id == data["id"]))
        return res.first()

    async def self_update(self, id_: int, db: AsyncSession, data: UserUpdate):
        if data.password is not None:
            data.password = pwd_context.hash(data.password)
        data_dict = data.model_dump(exclude={"id", "update_by"}, exclude_none=True)
        data_dict["hashed_password"] = data_dict.pop("password")
        if not data_dict:
            raise HTTPException(detail="Data is not full", status_code=403)
        stmt = (update(self.model).values(**data_dict).where(self.model.id == id_))
        await db.execute(stmt)
        await db.commit()
        stmt = select(self.model).where(self.model.id == id_)
        res = await db.scalar(stmt)
        return res

user_crud = UserCrud(UserModel)