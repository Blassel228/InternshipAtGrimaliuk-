from app.db.models.models import UserModel
from passlib.context import CryptContext
from sqlalchemy import update, delete, select
from app.schemas.schemas import UserUpdate
from app.repositories.repository import CrudRepository
from sqlalchemy.ext.asyncio import AsyncSession

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserRepository(CrudRepository):
    async def update(self, id_: int, db: AsyncSession, data: UserUpdate):
        if data.password is not None:
            data.password = pwd_context.hash(data.password)
        data_dict = data.model_dump(exclude={"id", "update_by"}, exclude_none=True)
        data_dict["hashed_password"] = data_dict.pop("password")
        if not data_dict:
            return None
        stmt = (update(self.model).values(**data_dict).where(self.model.id == id_))
        await db.execute(stmt)
        await db.commit()
        stmt = select(self.model).where(self.model.id == id_)
        res = await db.scalar(stmt)
        return res

    async def delete(self, db: AsyncSession, user_id: int):
        stmt = delete(self.model).where(self.model.id == user_id)
        res = await db.execute(stmt)
        if res.rowcount == 0:
            return None
        await db.commit()
        return res

user_repo = UserRepository(UserModel)
