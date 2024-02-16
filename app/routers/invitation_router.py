from fastapi import APIRouter, Depends
from app.utils.deps import get_db
from app.schemas.schemas import InvitationSchemaCreateIn
from app.CRUD.invitation_crud import invitation_crud
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.deps import get_current_user

invitation_router = APIRouter(tags=["invitation"], prefix="/invitation")

@invitation_router.post("/send_invitation")
async def send_invitation(db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user), invitation: InvitationSchemaCreateIn = None):
    return await invitation_crud.send_invitation(invitation=invitation, db=db, user_id=current_user.id)

@invitation_router.post("/accept_invitation")
async def accept_invitation(id_: int, db: AsyncSession = Depends(get_db),  current_user = Depends(get_current_user)):
    return await invitation_crud.accept_invitation(id_=id_, db=db, user_id=current_user.id)

@invitation_router.get("/get_received_invitations")
async def get_received_invitations(db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    return await invitation_crud.get_received_invitations(db=db, user_id=current_user.id)

@invitation_router.get("/get_all")
async def get_all(db: AsyncSession = Depends(get_db)):
    return await invitation_crud.get_all(db=db)

@invitation_router.get("/get_invited")
async def get_all(db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    return await invitation_crud.get_invited(db=db, user_id=current_user.id)

@invitation_router.delete("/reject_invitation")
async def reject_invitation(id_:int, current_user = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await invitation_crud.reject_invitation(id_=id_, user_id=current_user.id, db=db)