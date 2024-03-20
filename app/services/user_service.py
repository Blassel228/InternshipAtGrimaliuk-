from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.schemas import UserUpdate, User
from fastapi import HTTPException
from app.core.autho import pwd_context
from app.CRUD.user_crud import user_crud
class UserService:
    async def self_update(self, id_: int, db: AsyncSession, data: UserUpdate):
        if data.password is not None:
            data.password = pwd_context.hash(data.password)
        data_dict = data.model_dump(exclude={"id", "update_by"}, exclude_none=True)
        data_dict["hashed_password"] = data_dict.pop("password")
        if not data_dict:
            raise HTTPException(detail="Data is not full-filled", status_code=403)
        res = await user_crud.self_update(id_=id_, data=data_dict, db=db)
        return res

    async def delete(self, db: AsyncSession, id_: int):
        user = await user_crud.delete(id_=id_, db=db)
        if user is None:
            raise HTTPException(status_code=404, detail="The user is not valid")
        return user
    async def update(self, db: AsyncSession, id_: int, data: User):
        user = await user_crud.update(id_=id_, db=db, data=data)
        if user is None:
            raise HTTPException(status_code=404, detail="The user is not valid")
        return user

user_service = UserService()