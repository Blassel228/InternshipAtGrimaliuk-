from sqlalchemy.orm import Session
from app.CRUD.user_crud import user_crud
from app.schemas.schemas import UserUpdate
from fastapi import HTTPException
class UserService:
    async def update(self, db: Session, data: UserUpdate):
        user = await user_crud.update(id_=data.id, data=data, db=db)
        if user is None:
            raise HTTPException(status_code=404, detail="The user is not valid")
        return user

    async def delete(self, db: Session, user_id: int):
        user_id = await user_crud.delete(id_=user_id, db=db)
        if user_id is None:
            raise HTTPException(status_code=404, detail="The user is not valid")
        return user_id

user_service = UserService()