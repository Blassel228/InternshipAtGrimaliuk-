from app.repositories.repository import AbstractRepository
from app.schemas.schemas import User
from sqlalchemy.orm import Session
from app.repositories.repository import user_repo
class UserService:
    def get_all(self, db: Session):
        return user_repo.get_all(db=db)

    def get_one(self, id_: int, db: Session):
        return user_repo.get_one(id_=id_, db=db)

    def add_user(self, data: User, db:Session):
        data = data.model_dump()
        return user_repo.add(data=data, db=db)

    def update_user(self, id_: int, data: User, db: Session):
        data = data.model_dump()
        return user_repo.update(id_=id_, data=data, db=db)

    def delete_user(self, id_: int, db: Session):
        return user_repo.delete(id_=id_, db=db)
user_service = UserService()