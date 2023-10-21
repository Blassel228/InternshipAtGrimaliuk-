from fastapi import APIRouter, Depends
from app.db.models.models import get_db
from sqlalchemy.orm import Session
from app.schemas.schemas import User
from app.services.user import create_user, get_user, get_all_users, update_user, delete_user

user_router = APIRouter()

@user_router.put("/", tags=["user"])
async def update(db: Session = Depends(get_db), data: User = None, id_: int = None):
    return update_user(data, db = db, id_ = id_)

@user_router.delete("/", tags=["user"])
def delete(db: Session = Depends(get_db), id_: int = None):
    return delete_user(id_, db)

@user_router.get("{id}", tags=["user"])
async def get(id_: int = None, db: Session = Depends(get_db)):
    return get_user(id_, db)

@user_router.post("/", tags=["user"])
async def create(db: Session = Depends(get_db), data: User = None):
    return create_user(data, db)

@user_router.get("/", tags=["user"])
async def get_all(db: Session = Depends(get_db)):
    return get_all_users(db)