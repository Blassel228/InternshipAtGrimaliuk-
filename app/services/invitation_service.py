from fastapi import HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.models import CompanyModel, MemberModel, InvitationModel
from app.schemas.schemas import InvitationSchemaCreate, InvitationSchemaCreateIn
from fastapi import Depends
from app.utils.deps import get_db
from app.CRUD.company_crud import company_crud
from app.CRUD.user_crud import user_crud
from app.CRUD.invitation_crud import invitation_crud
from app.CRUD.member_crud import member_crud
class InvitationService:
    async def send_invitation(self, user_id: int, invitation: InvitationSchemaCreateIn, db: AsyncSession = Depends(get_db)):
        if invitation.recipient_id == user_id:
            raise HTTPException(status_code=404, detail="You cannot send invitation to yourself")
        stmt = select(CompanyModel).where(CompanyModel.owner_id == user_id)
        company = await db.scalar(stmt)
        if company is None:
            raise HTTPException(status_code=404, detail="You do not possess any company")
        invitation = InvitationSchemaCreate(owner_id=user_id, company_id=company.id, **invitation.model_dump())
        stmt = select(CompanyModel).where(CompanyModel.id == invitation.company_id)
        res = await db.scalar(stmt)
        if res is not None and res.owner_id == user_id:  # check if company is owned by user that are trying to send invitation
            stmt = insert(InvitationModel).values(**invitation.model_dump(exclude={"company_name"}))
            await db.execute(stmt)
            await db.commit()
        else:
            raise HTTPException(status_code=404, detail="You do not own such a company on behalf of which "
                                                        "you are trying to send the invitation")
        return invitation

    async def accept_invitation(self, id_: int, user_id: int, db: AsyncSession = Depends(get_db)):
        res = await user_crud.get_one(id_=user_id, db=db)
        stmt = select(MemberModel).where(MemberModel.id == res.id)
        res = await db.scalar(stmt)
        if res is not None:
            raise HTTPException(status_code=404, detail="You are in a company already")
        res = await invitation_crud.get_one(id_=id_, db=db)
        if res is None:
            raise HTTPException(status_code=404, detail="The invitation with such an id does not exist")
        if res.recipient_id != user_id:
            raise HTTPException(status_code=404, detail="You do not have such an invitation to accept")
        user = await user_crud.get_one(id_=user_id, db=db)
        company = await company_crud.get_one(id_=res.company_id, db=db)
        stmt = insert(MemberModel).values(company_id=company.id, id=user.id)
        await db.execute(stmt)
        member = await member_crud.get_one(id_=user.id, db=db)
        await invitation_crud.delete(id_=user.id, db=db)
        return member

    async def reject_invitation(self, id_: int, user_id: int, db: AsyncSession = Depends(get_db)):
        invitation = await invitation_crud.get_one(id_=id_, db=db)
        if invitation is None:
            raise HTTPException(status_code=404, detail="The invitation with such an id does not exist")
        if invitation.recipient_id != user_id:
            raise HTTPException(status_code=404, detail="You do not have such a invitation to delete")
        await invitation_crud.delete(id_=invitation.id, db=db)
        return invitation

    async def delete_by_owner(self, id_: int, user_id: int, db: AsyncSession = Depends(get_db)):
        res = await invitation_crud.get_one(id_=id_, db=db)
        if res is None:
            raise HTTPException(status_code=404, detail="The invitation with such an id does not exist")
        if user_id == res.owner_id:
            await invitation_crud.delete(id_=id_, db=db)
        else:
            raise HTTPException(status_code=404, detail="You do not possess such a company on behalf of which "
                                                        "the invitation was sent")
        return {"id_": id_}

invitation_service = InvitationService()