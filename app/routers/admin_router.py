from app.utils.deps import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.CRUD.admin_crud import admin_crud
from fastapi import APIRouter, Depends
from app.utils.deps import get_current_user

admin_router = APIRouter(tags=["admin"], prefix="/admin")

@admin_router.get("/get_all")
async def get_all(db: AsyncSession = Depends(get_db)):
    return await admin_crud.get_all(db=db)

@admin_router.post("/add")
async def add(id_: int, company_id: int, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    return await admin_crud.add(db=db, id_=id_, user_id=current_user.id, company_id=company_id)

@admin_router.delete("/delete")
async def delete(id_: int, company_id: int, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    return await admin_crud.delete(db=db, id_=id_, user_id=current_user.id, company_id=company_id)