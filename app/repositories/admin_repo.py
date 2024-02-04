from app.db.models.models import UserModel
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from sqlalchemy import insert, update
from app.repositories.repository import CrudRepository
from app.schemas.schemas import User
from sqlalchemy.ext.asyncio import AsyncSession

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AdminRepository(CrudRepository):

    async def add(self, db: AsyncSession, data: User):
        data = data.model_dump()
        stmt = insert(self.model).values(hashed_password=pwd_context.hash(data.pop("password")), **data)
        res = await db.execute(stmt)
        if res.rowcount==0:
            return None
        return data

    async def update(self, id_: int, db: AsyncSession, data: User):
        data = data.model_dump()
        stmt = (update(self.model).values(hashed_password=pwd_context.hash(data.pop("password")),**data).
                    where(self.model.id==id_))
        res = await db.execute(stmt)
        if res.rowcount==0:
            return None
        await db.commit()
        return data

admin_repo = AdminRepository(UserModel)