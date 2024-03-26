from sqlalchemy import insert, update, select, delete
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

class CrudRepository:
    def __init__(self, model):
        self.model = model

    async def get_all(self, db: AsyncSession):
        res = await db.scalars(select(self.model))
        return res.all()

    async def get_one(self, id_: int, db: AsyncSession):
        res = await db.scalars(select(self.model).where(self.model.id == id_))
        return res.first()

    async def add(self, db: AsyncSession, data: BaseModel):
        stmt = (insert(self.model).values(**data.model_dump()))
        res = await db.execute(stmt)
        if res.rowcount==0:
            return None
        await db.commit()
        res = await db.scalar(select(self.model).where(self.model.id == data.id))
        return res

    async def update(self, id_: int, db: AsyncSession, data: BaseModel):
        stmt = update(self.model).values(**data).where(self.model.id == id_)
        res = await db.execute(stmt)
        if res.rowcount==0:
            return None
        await db.commit()
        stmt = select(self.model).where(self.model.id == id_)
        res = await db.scalar(stmt)
        return res

    async def delete(self, id_: int, db: AsyncSession):
        stmt = select(self.model).where(self.model.id == id_)
        res = await db.scalar(stmt)
        if res is None:
            return None
        stmt = delete(self.model).where(self.model.id == id_)
        await db.execute(stmt)
        await db.commit()
        return res

    async def get_one_by_filter(self, db:AsyncSession, filters: dict):
        query = select(self.model).filter_by(**filters)
        result = await db.scalar(query)
        return result

    async def get_all_by_filter(self, db: AsyncSession, filters: dict):
        query = select(self.model).filter_by(**filters)
        result = await db.scalars(query)
        if result is None:
            raise HTTPException(status_code=404, detail="Not found")
        return result

    async def delete_all_by_filters(self, db: AsyncSession, filters: dict):
        result = await self.get_all_by_filter(filters=filters, db=db)
        if result is None:
            raise HTTPException(detail="Not found", status_code=404)
        query = delete(self.model).filter_by(**filters)
        await db.execute(query)
        return result
