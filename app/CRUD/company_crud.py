from fastapi import HTTPException
from sqlalchemy import update, select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.models import CompanyModel
from app.repositories.repository import CrudRepository
from app.schemas.schemas import CompanySchemaIn, CompanySchema

class CompanyCrud(CrudRepository):

    async def get_all_visible(self, db: AsyncSession):
        res = await db.scalars(select(self.model).where(self.model.visible == True))
        return res.all()

    async def get_one_visible(self, id_: int, db: AsyncSession):
        res = await db.scalar(select(self.model).where(self.model.id == id_ and self.model.visible == True))
        return res

    async def add(self, db: AsyncSession, data: CompanySchema):
        res = await db.scalar(select(self.model).where(self.model.id == data.id))
        if res is not None:
            raise HTTPException(status_code=404, detail="The company with such id already exist")
        stmt = (insert(self.model).values(**data.model_dump()))
        res = await db.execute(stmt)
        if res.rowcount==0:
            return None
        await db.commit()
        res = await self.get_one(db=db, id_=data.id)
        return res

    async def update(self, id_: int, user_id: int, db: AsyncSession, data: CompanySchemaIn): # noqa
        res = await self.get_one(db=db, id_=id_)
        if res is None:
            raise HTTPException(status_code=404, detail="Company you are trying to change does not exist")
        if user_id == res.owner_id:
            data = data.model_dump()
            stmt = update(self.model).values(data).where(self.model.owner_id == user_id)
            await db.execute(stmt)
        else:
            raise HTTPException(status_code=403, detail="You are trying to change company you do not own")
        await db.commit()
        res = await self.get_one(db=db, id_=data["id"])
        return res

    async def delete_by_owner(self, id_: int, user_id: int, db: AsyncSession): # noqa
        res = await self.get_one(db=db, id_=id_)
        if res is None:
            raise HTTPException(status_code=404, detail="Company you are trying to delete does not exist")
        if res.owner_id == user_id:
            res = await self.delete(db=db, id_=id_)
        else:
            raise HTTPException(status_code=403, detail="You do not possess company you are trying to delete")
        if res is None:
            raise HTTPException(status_code=404, detail="There is no such a company")
        await db.commit()
        return res

company_crud = CompanyCrud(CompanyModel)