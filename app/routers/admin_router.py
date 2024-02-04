from fastapi import APIRouter, Depends
from app.db.models.models import get_db
from sqlalchemy.orm import Session
from app.schemas.schemas import User#, UserIn
from app.services.admin_service import admin_service
from sqlalchemy.ext.asyncio import AsyncSession


admin_router = APIRouter(tags=["admin"])

@admin_router.put("/")
async def update(db: AsyncSession = Depends(get_db), data: User = None, id_: int = None):
    return await admin_service.update(id_=id_, db=db, data=data)

@admin_router.delete("/")
async def delete(db: AsyncSession = Depends(get_db), id_: int = None):
    return await admin_service.delete(id_=id_, db=db)

@admin_router.get("{id}")
async def get(id_: int = None, db: AsyncSession = Depends(get_db)):
    return await admin_service.get_one(id_=id_, db=db)

@admin_router.post("/")
async def create(db: AsyncSession = Depends(get_db), data: User = None):
    return await admin_service.add(db=db, data=data)
@admin_router.get("/")
async def get_all(db: AsyncSession = Depends(get_db)):
    return await admin_service.get_all(db=db)

