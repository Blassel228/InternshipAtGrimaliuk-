from app.db.models.models import UserModel
from sqlalchemy.orm import Session
from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy import update, delete
from app.core.autho import get_current_user
from typing import Annotated
from fastapi import Depends
from app.core.autho import oauth2_scheme

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserRepository():
    def __init__(self, model):
        self.model = model

    def self_update(self, db: Session, data: dict, token: Annotated[str, Depends(oauth2_scheme)]):
        user_id = get_current_user(token=token, db=db).id
        password = data.pop("password")
        stmt = (update(self.model).values(hashed_password=pwd_context.hash(password), username=data.get("username")).
                where(self.model.id == user_id))
        res = db.execute(stmt)
        if not res:
            raise HTTPException(status_code=404, detail="Query did not return anything")
        db.commit()
        return data

    def self_delete(self, db: Session, token: Annotated[str, Depends(oauth2_scheme)]):
        user_id = get_current_user(token=token, db=db).id
        stmt = delete(self.model).where(self.model.id == user_id)
        res = db.execute(stmt)
        if not res:
            raise HTTPException(status_code=404, detail="Query did not return anything")
        db.commit()
        return {"id": user_id}
user_repo = UserRepository(UserModel)