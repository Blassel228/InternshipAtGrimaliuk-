from app.db.models.models import UserModel
from passlib.context import CryptContext
from sqlalchemy import update, delete
from app.core.autho import get_current_user
from typing import Annotated
from fastapi import Depends
from app.core.autho import oauth2_scheme
from app.schemas.schemas import UserUpdate
from app.repositories.repository import CrudRepository
from sqlalchemy.ext.asyncio import AsyncSession

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserRepository(CrudRepository):

    async def update(self, db: AsyncSession, data: UserUpdate, token: Annotated[str, Depends(oauth2_scheme)]):
        user = await get_current_user(token=token, db=db)
        stmt = (update(self.model).values(hashed_password=pwd_context.hash(data.password), username=data.username).
                where(self.model.id == user.id))
        res = await db.execute(stmt)
        if res.rowcount==0:
            return None
        await db.commit()
        return data

    async def delete(self, db: AsyncSession, token: Annotated[str, Depends(oauth2_scheme)]):
        user_id = get_current_user(token=token, db=db).id
        stmt = delete(self.model).where(self.model.id == user_id)
        res = await db.execute(stmt)
        if res.rowcount==0:
            return None
        await db.commit()
        return {"id": user_id}
user_repo = UserRepository(UserModel)