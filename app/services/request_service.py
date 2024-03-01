from fastapi import HTTPException
from app.schemas.schemas import MemberSchema
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.schemas import RequestSchemaCreate, RequestSchemaCreateIn
from fastapi import Depends
from app.utils.deps import get_db
from app.CRUD.user_crud import user_crud
from app.CRUD.company_crud import company_crud
from app.CRUD.request_crud import request_crud
from app.CRUD.member_crud import member_crud

class RequestService:
    async def send_request(self, user_id: int, request: RequestSchemaCreateIn, db: AsyncSession = Depends(get_db)):
        res = await member_crud.get_one(id_=user_id, db=db)
        if res is not None:
            raise HTTPException(status_code=403, detail="You are in a company already")
        company = await company_crud.get_one(request.id, db=db)
        if company is None:
            raise HTTPException(status_code=404, detail="Such a company does not exist")
        if company.owner_id == user_id:
            raise HTTPException(status_code=403, detail="You cannot send request to company you own")
        res = await request_crud.get_one_by_filter(db=db, filters={"sender_id": user_id, "company_id": company.id})
        if res:
            raise HTTPException(status_code=409, detail="You have already sent request to that company")
        request = RequestSchemaCreate(**request.model_dump(), sender_id=user_id, company_id=company.id)
        await request_crud.add(data=request, db=db)
        return request

    async def accept_request(self, id_: int, user_id: int, db: AsyncSession = Depends(get_db)):
        request = await request_crud.get_one(id_=id_, db=db)
        if request is None:
            raise HTTPException(status_code=404, detail="The request with such an id does not exist")
        user = await user_crud.get_one(id_=request.sender_id, db=db)
        company = await company_crud.get_one_by_filter(db=db, filters={"owner_id": user_id})
        if company.owner_id != user_id:
            raise HTTPException(status_code=403, detail="You can not accept the request as you are not the owner")
        await request_crud.delete(id_=request.id, db=db)
        member = await member_crud.add(db=db, data=MemberSchema(company_id=company.id, id=user.id))
        return member

    async def reject_request(self, id_: int, user_id: int, db: AsyncSession = Depends(get_db)):
        request = await request_crud.get_one(id_=id_, db=db)
        if request is None:
            raise HTTPException(status_code=404, detail="The request with such an id does not exist")
        company = await company_crud.get_one(id_=request.company_id, db=db)
        if company.owner_id != user_id:
            raise HTTPException(status_code=403, detail="You do not own the company to reject the request")
        await request_crud.delete(id_=request.id, db=db)
        return request

    async def user_delete_its_request(self, id_: int, user_id: int, db: AsyncSession = Depends(get_db)):
        res = await request_crud.get_one(id_=id_, db=db)
        if res is None:
            raise HTTPException(status_code=404, detail="The request with such an id does not exist")
        if user_id == res.sender_id:
            res = await request_crud.delete(db=db, id_=id_)
        else:
            raise HTTPException(status_code=403, detail="You did not send request with such an id")
        return res

request_service = RequestService()