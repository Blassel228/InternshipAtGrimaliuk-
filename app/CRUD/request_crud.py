from fastapi import HTTPException
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.models import CompanyModel, RequestModel
from fastapi import Depends
from app.repositories.repository import CrudRepository
from app.utils.deps import get_db

class RequestCrud(CrudRepository):
    async def user_get_requests(self, user_id: int, db: AsyncSession):
        stmt = select(self.model).where(self.model.sender_id == user_id)
        res = await db.scalars(stmt)
        if res is None:
            raise HTTPException(status_code=404, detail="There is no requests you sent")
        return res.all()

    async def owner_get_requests(self, user_id: int, db: AsyncSession):
        stmt = select(CompanyModel).where(CompanyModel.owner_id == user_id)
        companies = await db.scalars(stmt)
        if companies is None:
            raise HTTPException(status_code=404, detail="You do not have requests because you do not own a company")
        requests = dict()
        for company in companies.all():
            stmt = select(self.model).where(self.model.company_id == company.id)
            res = await db.scalars(stmt)
            requests[f"{company.name}"] = res.all()
        if requests is None:
            raise HTTPException(status_code=404, detail="You do not have any request")
        return requests

request_crud = RequestCrud(RequestModel)