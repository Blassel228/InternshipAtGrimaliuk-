from fastapi import APIRouter, Depends
from app.utils.deps import get_db
from app.schemas.schemas import RequestSchemaCreate, RequestSchemaCreateIn
from app.CRUD.request_crud import request_crud
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.deps import get_current_user

invitation_router = APIRouter(tags=["request"], prefix="/request")

@invitation_router.post("/send_request")
async def send_request(db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user), invitation: RequestSchemaCreateIn = None):
    return await request_crud.send_request(invitation=invitation, db=db, user_id=current_user.id)
