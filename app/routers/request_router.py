from fastapi import APIRouter, Depends
from app.utils.deps import get_db
from app.schemas.schemas import User, RequestSchemaCreate, RequestSchemaCreateIn
from app.CRUD.request_crud import request_crud
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.deps import get_current_user

request_router = APIRouter(tags=["request"], prefix="/request")

@request_router.post("/send_request")
async def send_request(db: AsyncSession = Depends(get_db),  current_user = Depends(get_current_user), request: RequestSchemaCreateIn = None):
    return await request_crud.send_request(request=request, db=db, user_id=current_user.id)

@request_router.post("/accept_request")
async def accept_request(id_: int, db: AsyncSession = Depends(get_db),  current_user = Depends(get_current_user)):
    return await request_crud.accept_request(id_=id_, db=db, user_id=current_user.id)

@request_router.get("/get_all_owner_requests")
async def get_all_owner_requests(db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    return await request_crud.get_received_requests(db=db, user_id=current_user.id)

@request_router.get("/get_all")
async def get_all(db: AsyncSession = Depends(get_db)):
    return await request_crud.get_all(db=db)

@request_router.delete("/delete")
async def delete(id_:int, current_user = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await request_crud.delete(id_=id_, user_id=current_user.id, db=db)
