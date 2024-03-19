from app.db.models.models import UserModel
from sqlalchemy import update, select, insert
from app.repositories.repository import CrudRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.schemas import User, UserUpdate
from app.core.autho import pwd_context

class UserCrud(CrudRepository):
    async def update(self, id_: int, db: AsyncSession, data: User):
        data = data.model_dump()
        stmt = (update(self.model).values(hashed_password=pwd_context.hash(data.pop("password")),**data).
                where(self.model.id == id_))
        res = await db.execute(stmt)
        if res.rowcount==0:
            return None
        res = await self.get_one(id_=id_, db=db)
        await db.commit()
        return res

    async def self_update(self, id_: int, db: AsyncSession, data: dict):
        stmt = update(self.model).values(**data).where(self.model.id == id_)
        res = await db.execute(stmt)
        if res.rowcount == 0:
            return None
        await db.commit()
        stmt = select(self.model).where(self.model.id == id_)
        res = await db.scalar(stmt)
        return res

    async def add(self, db: AsyncSession, data: User):
        data = data.model_dump()
        stmt = insert(self.model).values(hashed_password=pwd_context.hash(data.pop("password")), **data)
        res = await db.execute(stmt)
        if res.rowcount == 0:
            return None
        await db.commit()
        res = await db.scalars(select(self.model).where(self.model.id == data["id"]))
        return res.first()

user_crud = UserCrud(UserModel)