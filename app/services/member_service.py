from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.CRUD.member_crud import member_crud
from app.CRUD.company_crud import company_crud
class MemberService:
    async def user_resign(self, db: AsyncSession, user_id: int):
        member = await member_crud.get_one(id_=user_id, db=db)
        if member is None:
            raise HTTPException(status_code=403, detail="You are not a member in any company")
        await member_crud.delete(id_=user_id, db=db)
        return member

    async def fire_user(self, id_: int, user_id: int, db: AsyncSession):
        company = await company_crud.get_one(id_=user_id, db=db)
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
        if company.owner_id != user_id:
            raise HTTPException(status_code=403, detail="You are not the owner of this company")
        member = await member_crud.get_one(id_=id_, db=db)
        if not member:
            raise HTTPException(status_code=404, detail="There is no such a member")
        await member_crud.delete(id_=id_, db=db)
        return member

    async def get_users_in_company(self, db: AsyncSession, user_id: int, company_id: int):
        company = await company_crud.get_one(id_=company_id, db=db)
        if company is None:
            raise HTTPException(status_code=404, detail="Company not found")
        if company.owner_id != user_id:
            raise HTTPException(status_code=403, detail="You do not own company")
        res = await member_crud.get_all_by_filter(filters={"company_id": company_id}, db=db)
        return res.all()

member_service = MemberService()