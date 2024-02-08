from app.schemas.schemas import CompanySchema, CompanySchemaIn
from app.db.models.models import get_db
from sqlalchemy import update, delete, insert, select
from app.db.models.models import CompanyModel
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.repository import CrudRepository

class CompanyCrud(CrudRepository):

    async def get_all(self, db: AsyncSession):
        res = await db.scalars(select(self.model).where(self.model.visible == True))
        return res.all()

    async def get_one(self, id_: int, db: AsyncSession):
        res = await db.scalars(select(self.model).where(self.model.id == id_ and self.model.visible == True))
        return res.first()

    async def update(self, id_company_to_change: int, user_id: int, db: AsyncSession, data: CompanySchemaIn): # noqa
        stmt = select(self.model).where(self.model.id == id_company_to_change)
        company_to_change = await db.scalar(stmt)
        if user_id == company_to_change.owner_id:
            data = data.model_dump()
            stmt = update(self.model).values(data).where(self.model.owner_id== user_id)
            res = await db.execute(stmt)
        else:
            raise HTTPException(status_code=404, detail="You are trying to change company you do not own")
        if res.rowcount==0:
            raise HTTPException(status_code=404, detail="Company you are trying to change does not exist")
        await db.commit()
        stmt = select(self.model).where(self.model.id == data["id"])
        res = await db.scalar(stmt)
        return res

    async def delete(self, id_: int, user_id: int, db: AsyncSession): # noqa
        stmt = select(self.model).where(self.model.id == id_)
        company_to_delete = await db.scalar(stmt)
        if company_to_delete is None:
            raise HTTPException(status_code=404, detail="Company you are trying to delete does not exist")
        if company_to_delete.owner_id == user_id:
            stmt = delete(self.model).where(self.model.id == id_)
            res = await db.execute(stmt)
        else:
            raise HTTPException(status_code=404, detail="You do not possess company you are trying to delete")
        if res.rowcount==0:
            return None
        await db.commit()
        return {"id": id_}

company_crud = CompanyCrud(CompanyModel)