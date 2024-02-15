from fastapi import HTTPException
from sqlalchemy import update, delete, select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.models import CompanyModel, RequestModel, UserModel
from app.schemas.schemas import RequestSchemaCreate, RequestSchemaCreateIn
from fastapi import Depends
from app.repositories.repository import CrudRepository
from app.utils.deps import get_db

class RequestCrud(CrudRepository):
    async def send_request(self, user_id: int, request: RequestSchemaCreateIn, db: AsyncSession = Depends(get_db)):
        stmt = select(CompanyModel).where(CompanyModel.name == request.company_name)
        company = await db.scalar(stmt)
        if company is None:
            raise HTTPException(status_code=404, detail="Such a company does not exist")
        if company.company_id == user_id:
            raise HTTPException(status_code=404, detail="You cannot send request to company you own")
        request = RequestSchemaCreate(sender_id=user_id, company_id=company.company_id, **request.model_dump())
        stmt = insert(self.model).values(**request.model_dump(exclude={"company_name"}))
        await db.execute(stmt)
        await db.commit()
        return request

    async def delete(self, id_: int, user_id: int, db: AsyncSession = Depends(get_db)):
        stmt = select(self.model).where(self.model.request_id == id_)
        res = await db.scalar(stmt)
        if res is None:
            raise HTTPException(status_code=404, detail="The request with such an id does not exist")
        if user_id == res.sender_id:
            stmt = delete(self.model).where(self.model.invitation_id == id_)
            await db.execute(stmt)
            await db.commit()
        else:
            raise HTTPException(status_code=404, detail="You did not send request with such an id")
        return {"id_": id_}

    async def accept_request(self, id_: int, user_id: int, db: AsyncSession = Depends(get_db)):
        stmt = select(self.model).where(self.model.request_id == id_)
        request = await db.scalar(stmt)
        if request is None:
            raise HTTPException(status_code=404, detail="The request with such an id does not exist")
        stmt = select(UserModel).where(self.model.sender_id == user_id)
        user = await db.scalar(stmt)
        stmt = select(CompanyModel).where(self.model.company_id == request.company_id)
        company = await db.scalar(stmt)
        if company.owner_id != user_id:
            raise HTTPException(status_code=404, detail="You can not accept the request as you are not the owner")
        await company.members.append(user)
        stmt = delete(self.model).where(self.model.request_id == request.request_id)
        await db.execute(stmt)
        await db.commit()
        return {f"User {user} was added to company {company.name}"}

    async def reject_request(self, id_: int, user_id: int, db: AsyncSession = Depends(get_db)):
        stmt = select(self.model).where(self.model.request_id == id_)
        request = await db.scalar(stmt)
        if request is None:
            raise HTTPException(status_code=404, detail="The request with such an id does not exist")
        stmt = select(CompanyModel).where(CompanyModel.company_id == request.company_id)
        company = await db.scalar(stmt)
        if company.owner_id != user_id:
            raise HTTPException(status_code=404, detail="You do not own the company to reject the request")
        stmt = delete(self.model).where(self.model.invitation_id == request.invitation_id)
        await db.execute(stmt)
        await db.commit()
        return request

request_crud = RequestCrud(RequestModel)