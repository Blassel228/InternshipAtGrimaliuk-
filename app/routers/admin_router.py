from fastapi import APIRouter, Depends
from app.db.models.models import get_db
from sqlalchemy.orm import Session
from app.schemas.schemas import User
from app.services.admin_service import admin_service


admin_router = APIRouter(tags=["admin"])

@admin_router.put("/")
async def update(db: Session = Depends(get_db), data: User = None, id_: int = None):
    return admin_service.update_user(id_=id_, db=db, data=data)

@admin_router.delete("/")
def delete(db: Session = Depends(get_db), id_: int = None):
    return admin_service.delete_user(id_=id_, db=db)

@admin_router.get("{id}")
async def get(id_: int = None, db: Session = Depends(get_db)):
    return admin_service.get_one(id_=id_, db=db)

@admin_router.post("/")
async def create(db: Session = Depends(get_db), data: User = None):
    return admin_service.add_user(db=db, data=data)
@admin_router.get("/")
async def get_all(db: Session = Depends(get_db)):
    return admin_service.get_all(db=db)

