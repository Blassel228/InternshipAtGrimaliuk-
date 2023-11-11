from app.db.models.models import UserModel
from sqlalchemy.orm import Session
from fastapi import HTTPException
from passlib.context import CryptContext
from abc import ABC, abstractmethod
from sqlalchemy import insert, update, select, delete

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
class AbstractRepository(ABC):
    @abstractmethod
    def get_all(self):
        raise NotImplementedError

    @abstractmethod
    def get_one(self):
        raise NotImplementedError

    @abstractmethod
    def update(self):
        raise NotImplementedError

    @abstractmethod
    def add(self):
        raise NotImplementedError

class CrudRepository(AbstractRepository):
    def __init__(self, model):
        self.model = model

    def get_all(self, db: Session):
        return db.execute(select(self.model)).scalars().all()

    def get_one(self, id_: int, db: Session):
        return db.execute(select(self.model).where(self.model.id==id_)).scalar()

    def add(self, db: Session, data: dict):
        if "password" in data:
            password = data.pop("password")
            stmt = (insert(self.model).values(hashed_password=pwd_context.hash(password), **data))
        else:
            stmt = (insert(self.model).values(**data))
        res = db.execute(stmt)
        if not res:
            raise HTTPException(status_code=404, detail="Query did not return anything")
        db.commit()
        return data

    def update(self, id_: int, db: Session, data: dict):
        if "password" in data:
            password = data.pop("password")
            stmt = (update(self.model).values(hashed_password=pwd_context.hash(password),**data).
                    where(self.model.id==id_))
        else:
            stmt = update(self.model).values(**data).where(self.model.id==id_)
        res = db.execute(stmt)
        if not res:
            raise HTTPException(status_code=404, detail="Query did not return anything")
        db.commit()
        return data

    def delete(self, id_: int, db: Session):
        stmt = delete(self.model).where(self.model.id==id_)
        res = db.execute(stmt)
        if not res:
            raise HTTPException(status_code=404, detail="Query did not return anything")
        db.commit()
        return {"id":id_}

user_repo = CrudRepository(UserModel)