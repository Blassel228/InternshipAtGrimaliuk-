from sqlalchemy.orm import Session
from app.repositories.user_repo import user_repo
from app.schemas.schemas import UserUpdate
from typing import Annotated
from fastapi import Depends
from app.core.autho import oauth2_scheme
class UserService:
    def self_update(self, db: Session, token: Annotated[str, Depends(oauth2_scheme)], data: UserUpdate):
        data = data.model_dump()
        return user_repo.self_update(data=data, token=token, db=db)

    def self_delete(self, db: Session, token: Annotated[str, Depends(oauth2_scheme)]):
        return user_repo.self_delete(token=token, db=db)

user_service = UserService()