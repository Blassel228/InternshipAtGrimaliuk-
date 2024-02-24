from fastapi import APIRouter, Depends
from app.utils.deps import get_db
from app.schemas.schemas import RequestSchemaCreateIn
from app.CRUD.request_crud import request_crud
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.deps import get_current_user
from app.services.request_service import request_service

request_router = APIRouter(tags=["request"], prefix="/request")

@request_router.post("/send_request")
async def send_request(db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user), request: RequestSchemaCreateIn = None):
    return await request_service.send_request(request=request, db=db, user_id=current_user.id)

@request_router.delete("/user_delete_its_request")
async def delete(id_: int, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    return await request_service.user_delete_its_request(id_=id_, db=db, user_id=current_user.id)

@request_router.post("/accept_request")
async def accept_request(id_: int, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    return await request_service.accept_request(id_=id_, db=db, user_id=current_user.id)

@request_router.delete("/reject_request")
async def reject_request(id_: int, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    return await request_service.reject_request(id_=id_, db=db, user_id=current_user.id)

@request_router.get("/user_get_requests", tags=["user"])
async def user_get_requests(db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    return await request_crud.user_get_requests(db=db, user_id=current_user.id)

@request_router.get("/owner_get_requests")
async def user_get_requests(db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    return await request_crud.owner_get_requests(db=db, user_id=current_user.id)