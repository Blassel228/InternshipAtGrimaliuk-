from fastapi import APIRouter, Depends
from app.utils.deps import get_db
from app.schemas.schemas import RequestSchemaCreate, RequestSchemaCreateIn
from app.CRUD.request_crud import request_crud
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.deps import get_current_user

request_router = APIRouter(tags=["request"], prefix="/request")

@request_router.post("/send_request")
async def send_request(db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user), invitation: RequestSchemaCreateIn = None):
    return await request_crud.send_request(invitation=invitation, db=db, user_id=current_user.id)

@request_router.delete("/delete")
async def send_request(id_: int, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    return await request_crud.delete(id_=id_, db=db, user_id=current_user.id)

@request_router.post("/accept_request")
async def accept_request(id_: int, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    return await request_crud.accept_request(id_=id_, db=db, user_id=current_user.id)

@request_router.delete("/reject_request")
async def reject_request(id_: int, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    return await request_crud.reject_request(id_=id_, db=db, user_id=current_user.id)

@request_router.get("/user_get_requests", tags=["user"])
async def user_get_requests(db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    return await request_crud.user_get_requests(db=db, user_id=current_user.id)

@request_router.get("/owner_get_requests")
async def user_get_requests(db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    return await request_crud.owner_get_requests(db=db, user_id=current_user.id)