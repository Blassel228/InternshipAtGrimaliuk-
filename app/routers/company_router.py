from fastapi import APIRouter, Depends
from app.utils.deps import get_current_user, get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.CRUD.company_crud import company_crud
from app.schemas.schemas import CompanySchemaIn, CompanySchema

company_router = APIRouter(tags=["company"], prefix="/company")

@company_router.get("/get_companies")
async def select_company(db: AsyncSession = Depends(get_db)):
    return await company_crud.get_all(db=db)

@company_router.get("/get_company")
async def select_company(id_: int, db: AsyncSession = Depends(get_db)):
    return await company_crud.get_one(id_=id_, db=db)

@company_router.post("/create_company")
async def create_company(data: CompanySchemaIn, current_user = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await company_crud.add(db=db, data=CompanySchema(**data.model_dump(), owner_id=current_user.id))

@company_router.delete("/delete_company")
async def delete_company(id_: int, current_user = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await company_crud.delete(id_=id_, db=db, user_id = current_user.id)

@company_router.put("/update_company")
async def update_company(id_: int, data: CompanySchemaIn, current_user = Depends(get_current_user),  db: AsyncSession = Depends(get_db)):
    return await company_crud.update(db=db, data=data, user_id=current_user.id, id_=id_)

@company_router.delete("/fire_user")
async def fire_user(id_: int, data: CompanySchemaIn, current_user = Depends(get_current_user),  db: AsyncSession = Depends(get_db)):
    return await company_crud.fire_user(db=db, data=data, user_id=current_user.id, id_=id_)
