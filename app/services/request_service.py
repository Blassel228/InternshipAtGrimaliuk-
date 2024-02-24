from fastapi import HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.models import CompanyModel, MemberModel, RequestModel
from app.schemas.schemas import RequestSchemaCreate, RequestSchemaCreateIn
from fastapi import Depends
from app.utils.deps import get_db
from app.CRUD.user_crud import user_crud
from app.CRUD.company_crud import company_crud
from app.CRUD.request_crud import request_crud
from app.CRUD.member_crud import member_crud

class RequestService:
    async def send_request(self, user_id: int, request: RequestSchemaCreateIn, db: AsyncSession = Depends(get_db)):
        stmt = select(MemberModel).where(MemberModel.id == user_id)
        res = await db.scalar(stmt)
        if res is not None:
            raise HTTPException(status_code=404, detail="You are in a company already")
        company = await company_crud.get_one(request.id, db=db)
        if company is None:
            raise HTTPException(status_code=404, detail="Such a company does not exist")
        if company.owner_id == user_id:
            raise HTTPException(status_code=404, detail="You cannot send request to company you own")
        stmt = select(RequestModel).where(RequestModel.sender_id == user_id and RequestModel.id == company.id)
        res = await db.scalar(stmt)
        if res is not None:
            raise HTTPException(status_code=404, detail="You have already sent request to that company")
        request = RequestSchemaCreate(**request.model_dump(), sender_id=user_id, company_id=company.id)
        await request_crud.add(data=request, db=db)
        return request

    async def accept_request(self, id_: int, user_id: int, db: AsyncSession = Depends(get_db)):
        request = await request_crud.get_one(id_=id_, db=db)
        if request is None:
            raise HTTPException(status_code=404, detail="The request with such an id does not exist")
        user = await user_crud.get_one(id_=request.sender_id, db=db)
        stmt = select(CompanyModel).where(CompanyModel.owner_id == user_id)
        company = await db.scalar(stmt)
        if company.owner_id != user_id:
            raise HTTPException(status_code=404, detail="You can not accept the request as you are not the owner")
        stmt = insert(MemberModel).values(company_id=company.id, id=user.id)
        await db.execute(stmt)
        member = await member_crud.get_one(id_=user.id, db=db)
        await request_crud.delete(id_=request.id, db=db)
        return member

    async def reject_request(self, id_: int, user_id: int, db: AsyncSession = Depends(get_db)):
        request = await request_crud.get_one(id_=id_, db=db)
        if request is None:
            raise HTTPException(status_code=404, detail="The request with such an id does not exist")
        company = await company_crud.get_one(id_=request.company_id, db=db)
        if company.owner_id != user_id:
            raise HTTPException(status_code=404, detail="You do not own the company to reject the request")
        await request_crud.delete(id_=request.id, db=db)
        return request

    async def user_delete_its_request(self, id_: int, user_id: int, db: AsyncSession = Depends(get_db)):
        res = await request_crud.get_one(id_=id_, db=db)
        if res is None:
            raise HTTPException(status_code=404, detail="The request with such an id does not exist")
        if user_id == res.sender_id:
            await request_crud.delete(db=db, id_=id_)
        else:
            raise HTTPException(status_code=404, detail="You did not send request with such an id")
        return {"id_": id_}

request_service = RequestService()