from app.schemas.schemas import User
from sqlalchemy.orm import Session
from app.repositories.admin_repo import admin_repo
class AdminService:
    def get_all(self, db: Session):
        return admin_repo.get_all(db=db)

    def get_one(self, id_: int, db: Session):
        return admin_repo.get_one(id_=id_, db=db)

    def add_user(self, data: User, db:Session):
        data = data.model_dump()
        return admin_repo.add(data=data, db=db)

    def update_user(self, id_: int, data: User, db: Session):
        data = data.model_dump()
        return admin_repo.update(id_=id_, data=data, db=db)

    def delete_user(self, id_: int, db: Session):
        return admin_repo.delete(id_=id_, db=db)

admin_service = AdminService()