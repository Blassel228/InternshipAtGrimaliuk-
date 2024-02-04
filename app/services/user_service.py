from sqlalchemy.orm import Session
from app.repositories.user_repo import user_repo
from app.schemas.schemas import UserUpdate
from typing import Annotated
from fastapi import Depends, HTTPException
from app.core.autho import oauth2_scheme
class UserService:
    async def update(self, db: Session, token: Annotated[str, Depends(oauth2_scheme)], data: UserUpdate):
        user = await user_repo.update(data=data, token=token, db=db)
        if user is None:
            raise HTTPException(status_code=404, detail="The user is not valid")
        return user

    async def delete(self, db: Session, token: Annotated[str, Depends(oauth2_scheme)]):
        user_id = await user_repo.delete(token=token, db=db)
        if user_id is None:
            raise HTTPException(status_code=404, detail="The user is not valid")
        return user_id

user_service = UserService()