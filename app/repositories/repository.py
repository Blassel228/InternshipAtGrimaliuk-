from sqlalchemy import insert, update, select, delete
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession, AsyncResult
from sqlalchemy.orm import Session
class CrudRepository:
    def __init__(self, model):
        self.model = model

    async def get_all(self, db: AsyncSession):
        res = await db.scalars(select(self.model))
        return res.all()

    async def get_one(self, id_: int, db: AsyncSession):
        res = await db.scalars(select(self.model).where(id_==self.model.id))
        return res.first()

    async def add(self, db: AsyncSession, data: BaseModel):
        data = data.model_dump()
        stmt = (insert(self.model).values(**data))
        res = await db.execute(stmt)
        if res.rowcount==0:
            return None
        await db.commit()
        return res.first()

    async def update(self, id_: int, db: AsyncSession, data: BaseModel):
        stmt = update(self.model).values(**data).where(self.model.id == id_)
        res = await db.execute(stmt)
        if res.rowcount==0:
            return None
        await db.commit()
        return data

    async def delete(self, id_: int, db: AsyncSession):
        stmt = delete(self.model).where(self.model.id == id_)
        res = await db.execute(stmt)
        if res.rowcount==0:
            return None
        await db.commit()
        return {"id": id_}