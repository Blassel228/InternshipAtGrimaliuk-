from fastapi import HTTPException
from sqlalchemy import delete, select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.models import CompanyModel, InvitationModel, UserModel, MemberModel
from app.schemas.schemas import InvitationSchemaCreate, InvitationSchemaCreateIn
from fastapi import Depends
from app.repositories.repository import CrudRepository
from app.utils.deps import get_db

class InvitationCrud(CrudRepository):
    async def get_received_invitations(self, user_id: int, db: AsyncSession = Depends(get_db)):
        invitations = await db.scalars(select(self.model).where(self.model.recipient_id == user_id))
        if invitations is None:
            raise HTTPException(status_code=404, detail="Users were not found")
        return invitations.all()

    async def send_invitation(self, user_id: int, invitation: InvitationSchemaCreateIn, db: AsyncSession = Depends(get_db)):
        if invitation.recipient_id == user_id:
            raise HTTPException(status_code=404, detail="You cannot send invitation to yourself")
        stmt = select(CompanyModel).where(CompanyModel.owner_id == user_id)
        company = await db.scalar(stmt)
        if company is None:
            raise HTTPException(status_code=404, detail="You do not possess any company")
        invitation = InvitationSchemaCreate(owner_id=user_id, company_id=company.company_id, **invitation.model_dump())
        stmt = select(CompanyModel).where(CompanyModel.name == invitation.company_name)
        res = await db.scalar(stmt)
        if res.owner_id == user_id: #check if company is owned by user that are trying to send invitation
            stmt = insert(self.model).values(**invitation.model_dump(exclude={"company_name"}))
            await db.execute(stmt)
            await db.commit()
        else:
            raise HTTPException(status_code=404, detail="You do not own such a company on behalf of which "
                                                        "you are trying to send the invitation")
        return invitation

    async def delete(self, id_: int, user_id: int, db: AsyncSession = Depends(get_db)):
        stmt = select(self.model).where(self.model.id == id_)
        res = await db.scalar(stmt)
        if res is None:
            raise HTTPException(status_code=404, detail="The invitation with such an id does not exist")
        if user_id == res.owner_id:
            stmt = delete(self.model).where(self.model.id == id_)
            await db.execute(stmt)
            await db.commit()
        else:
            raise HTTPException(status_code=404, detail="You do not possess such a company on behalf of which "
                                                        "the invitation was sent")
        return {"id_": id_}

    async def accept_invitation(self, id_: int, user_id: int, db: AsyncSession = Depends(get_db)):
        stmt = select(UserModel).where(UserModel.id == user_id)
        res = await db.scalar(stmt)
        stmt = select(MemberModel).where(MemberModel.mail == res.mail)
        res = db.execute(stmt)
        if res is not None:
            raise HTTPException(status_code=404, detail="You are in a company already")
        stmt = select(self.model).where(self.model.id == id_)
        res = await db.scalar(stmt)
        if res is None:
            raise HTTPException(status_code=404, detail="The invitation with such an id does not exist")
        if res.recipient_id != user_id:
            raise HTTPException(status_code=404, detail="You do not have such an invitation to accept")
        stmt = select(UserModel).where(self.model.recipient_id == user_id)
        user = await db.scalar(stmt)
        stmt = select(CompanyModel).where(self.model.id == res.company_id)
        company = await db.scalar(stmt)
        stmt = insert(MemberModel).values(company_id=company.company_id, company_name=company.name,
                                          mail=user.mail, name=user.username)
        await db.execute(stmt)
        stmt = delete(self.model).where(self.model.id == res.invitation_id)
        await db.execute(stmt)
        await db.commit()
        return f"{user} was added to {company.name}"

    async def reject_invitation(self, id_: int, user_id: int, db: AsyncSession = Depends(get_db)):
        stmt = select(self.model).where(self.model.id == id_)
        invitation = await db.scalar(stmt)
        if invitation is None:
            raise HTTPException(status_code=404, detail="The invitation with such an id does not exist")
        if invitation.recipient_id != user_id:
            raise HTTPException(status_code=404, detail="You do not have such a invitation to delete")
        stmt = delete(self.model).where(self.model.id == invitation.invitation_id)
        await db.execute(stmt)
        await db.commit()
        return invitation

    async def get_invited(self, user_id: int, db: AsyncSession):
        stmt = select(self.model).where(self.model.owner_id == user_id)
        res = await db.scalars(stmt)
        if res is None:
            raise HTTPException(status_code=404, detail="You did not send any invitation")
        return res.all()

invitation_crud = InvitationCrud(InvitationModel)