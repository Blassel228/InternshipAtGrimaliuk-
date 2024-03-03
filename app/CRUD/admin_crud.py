from app.db.models.models import AdminModel
from app.repositories.repository import CrudRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.CRUD.member_crud import member_crud
from app.CRUD.company_crud import company_crud
from fastapi import HTTPException
from sqlalchemy import insert, delete, select

class AdminCrud(CrudRepository):
    async def add(self, id_: int, company_id: int, user_id: int, db: AsyncSession):
        company = await company_crud.get_one_by_filter(db=db, filters={"id": company_id})
        if company is None:
            raise HTTPException(status_code=404, detail="There is no such a company")
        if company.owner_id != user_id:
            raise HTTPException(status_code=403, detail="You do not own such a company")
        member = await member_crud.get_one(db=db, id_=id_)
        if member is None:
            raise HTTPException(status_code=404, detail="There is no such a member")
        if member.company_id != company.id:
            raise HTTPException(status_code=403, detail="This user is not in your company")
        stmt = insert(self.model).values(id=id_)
        await db.execute(stmt)
        await db.commit()
        admin = await admin_crud.get_one(db=db, id_=id_)
        if admin is None:
            raise HTTPException(status_code=500, detail="Admin was not added for some reason")
        return admin

    async def delete(self, id_: int, company_id: int, user_id: int, db: AsyncSession):
        company = await company_crud.get_one_by_filter(db=db, filters={"id": company_id})
        if company is None:
            raise HTTPException(status_code=404, detail="There is no such a company")
        if company.owner_id != user_id:
            raise HTTPException(status_code=403, detail="You do not own such a company")
        member = await member_crud.get_one(db=db, id_=id_)
        admin = await self.get_one(db=db, id_=id_)
        if admin is None:
            raise HTTPException(status_code=404, detail="There is no such an admin")
        if member.company_id != company.id:
            raise HTTPException(status_code=403, detail="This admin is not in your company")
        stmt = delete(self.model).where(self.model.id == id_)
        await db.execute(stmt)
        await db.commit()
        return admin

admin_crud = AdminCrud(AdminModel)