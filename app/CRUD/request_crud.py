from fastapi import HTTPException
from sqlalchemy import update, delete, select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.models import CompanyModel, RequestModel, UserModel
from app.schemas.schemas import RequestSchemaCreate, RequestSchemaCreateIn
from fastapi import Depends
from app.repositories.repository import CrudRepository
from app.utils.deps import get_db

class RequestCrud(CrudRepository):
    async def get_received_requests(self, user_id: int, db: AsyncSession = Depends(get_db)):
        requests = await db.scalars(select(self.model).where(self.model.recipient_id == user_id))
        if requests is None:
            raise HTTPException(status_code=404, detail="Users were not found")
        return requests.all()

    async def send_request(self, user_id: int,  request: RequestSchemaCreateIn, db: AsyncSession = Depends(get_db)):
        stmt = select(CompanyModel).where(CompanyModel.owner_id == user_id)
        company = await db.scalar(stmt)
        if company is None:
            raise HTTPException(status_code=404, detail="You do not possess any company")
        request = RequestSchemaCreate(owner_id=user_id, company_id=company.company_id, **request.model_dump())
        stmt = select(CompanyModel).where(CompanyModel.name == request.company_name)
        res = await db.scalar(stmt)
        if res.owner_id == user_id: #check if company is owned by user that are trying to send request
            stmt = insert(self.model).values(**request.model_dump(exclude={"company_name"}))
            await db.execute(stmt)
            await db.commit()
        else:
            raise HTTPException(status_code=404, detail="You do not own such a company on behalf of which "
                                                        "you are trying to send the invitation")
        return request

    async def delete(self, id_: int, user_id: int, db: AsyncSession = Depends(get_db)):
        stmt = select(self.model).where(self.model.request_id == id_)
        res = await db.scalar(stmt)
        if res is None:
            raise HTTPException(status_code=404, detail="The request with such an id does not exist")
        if user_id == res.owner_id:
            stmt = delete(self.model).where(self.model.request_id == id_)
            await db.execute(stmt)
            await db.commit()
        else:
            raise HTTPException(status_code=404, detail="You do not possess such a company on behalf of which "
                                                        "the request was sent")
        return {"id_": id_}

    async def accept_request(self, id_: int, user_id: int, db: AsyncSession = Depends(get_db)):
        stmt = select(self.model).where(self.model.request_id == id_)
        res = await db.scalar(stmt)
        if res is None:
            raise HTTPException(status_code=404, detail="The request with such an id does not exist")
        if res.recipient_id != user_id:
            raise HTTPException(status_code=404, detail="You do not have such a request to accept")
        stmt = select(UserModel).where(self.model.recipient_id == user_id)
        user = await db.scalar(stmt)
        stmt = select(CompanyModel).where(self.model.company_id == res.company_id)
        company = await db.scalar(stmt)
        company.members.append(user)
        stmt = delete(self.model).where(self.model.id == res.request_id)
        await db.execute(stmt)
        await db.commit()
        return {f"User {user} was added to company {company.name}"}

request_crud = RequestCrud(RequestModel)