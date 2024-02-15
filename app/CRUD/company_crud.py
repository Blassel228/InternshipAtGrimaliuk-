from fastapi import HTTPException, status
from sqlalchemy import update, delete, select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.models import CompanyModel, UserModel
from app.repositories.repository import CrudRepository
from app.schemas.schemas import CompanySchemaIn, CompanySchema


class CompanyCrud(CrudRepository):

    async def get_all(self, db: AsyncSession):
        res = await db.scalars(select(self.model).where(self.model.visible == True))
        return res.all()

    async def get_one(self, id_: int, db: AsyncSession):
        res = await db.scalars(select(self.model).where(self.model.company_id == id_ and self.model.visible == True))
        return res.first()

    async def add(self, db: AsyncSession, data: CompanySchema):
        res = await db.scalar(select(self.model).where(self.model.company_id == data.company_id))
        if res is not None:
            raise HTTPException(status_code=404, detail="The company with such id already exsit")
        stmt = (insert(self.model).values(**data.model_dump()))
        res = await db.execute(stmt)
        if res.rowcount==0:
            return None
        await db.commit()
        res = await db.scalar(select(self.model).where(self.model.company_id==data.company_id))
        return res

    async def update(self, id_: int, user_id: int, db: AsyncSession, data: CompanySchemaIn): # noqa
        stmt = select(self.model).where(self.model.company_id == id_)
        company_to_change = await db.scalar(stmt)
        if company_to_change is None:
            raise HTTPException(status_code=404, detail="Company you are trying to change does not exist")
        if user_id == company_to_change.owner_id:
            data = data.model_dump()
            stmt = update(self.model).values(data).where(self.model.owner_id== user_id)
            await db.execute(stmt)
        else:
            raise HTTPException(status_code=404, detail="You are trying to change company you do not own")
        await db.commit()
        stmt = select(self.model).where(self.model.company_id == data["id"])
        res = await db.scalar(stmt)
        return res

    async def delete(self, id_: int, user_id: int, db: AsyncSession): # noqa
        stmt = select(self.model).where(self.model.company_id == id_)
        company_to_delete = await db.scalar(stmt)
        if company_to_delete is None:
            raise HTTPException(status_code=404, detail="Company you are trying to delete does not exist")
        if company_to_delete.owner_id == user_id:
            stmt = delete(self.model).where(self.model.company_id == id_)
            res = await db.execute(stmt)
        else:
            raise HTTPException(status_code=404, detail="You do not possess company you are trying to delete")
        if res.rowcount==0:
            return None
        await db.commit()
        return {"id": id_}

    async def fire_user(self, company_id: int, id_: int, user_id: int, db: AsyncSession):
        # Check if the current user owns the company
        company = await db.get(CompanyModel, company_id)
        if not company:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
        if company.owner_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not the owner of this company")
        user_to_remove = await db.get(UserModel, id_)
        if not user_to_remove:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        if user_to_remove in company.members:
            company.members.remove(user_to_remove)
            await db.commit()
            return {"message": f"User {user_to_remove.username} removed from company {company.name}"}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User is not a member of this company")

    async def user_resign(self, db: AsyncSession, user_id: int):
        stmt = delete(UserModel).where(self.model.id == user_id)
        user = await db.execute(stmt)
        stmt = select(CompanyModel).where(user.companies[0] == CompanyModel.name)
        company = await db.execute(stmt)
        company.members.remove(user)
        await db.commit()
        return user

    async def get_users_in_company(self, db: AsyncSession, user_id: int, company_name: str):
        stmt = select(CompanyModel).where(self.model.name == company_name)
        company = await db.execute(stmt)
        if company is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
        if company.owner_id != user_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You do not own company")
        await db.commit()
        return company.members

company_crud = CompanyCrud(CompanyModel)