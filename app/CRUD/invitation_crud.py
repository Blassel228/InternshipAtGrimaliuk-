from fastapi import HTTPException
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.models import InvitationModel
from fastapi import Depends
from app.repositories.repository import CrudRepository
from app.utils.deps import get_db

class InvitationCrud(CrudRepository):
    async def get_received_invitations(self, user_id: int, db: AsyncSession = Depends(get_db)):
        invitations = await db.scalars(select(self.model).where(self.model.recipient_id == user_id))
        if invitations is None:
            raise HTTPException(status_code=404, detail="Users were not found")
        return invitations.all()

    async def get_invited(self, user_id: int, db: AsyncSession):
        stmt = select(self.model).where(self.model.owner_id == user_id)
        res = await db.scalars(stmt)
        if res is None:
            raise HTTPException(status_code=404, detail="You did not send any invitation")
        return res.all()

invitation_crud = InvitationCrud(InvitationModel)