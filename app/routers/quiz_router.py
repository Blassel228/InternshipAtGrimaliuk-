from app.CRUD.quiz_crud import quiz_crud
from app.schemas.schemas import QuizCreate
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, APIRouter
from app.utils.deps import get_db
from app.utils.deps import get_current_user

quiz_router = APIRouter(tags=["quiz"])

@quiz_router.post("/create")
async def create_quiz(quiz: QuizCreate, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    return await quiz_crud.create(db=db, quiz=quiz, user_id=current_user.id)

@quiz_router.put("/update")
async def update_quiz(id_:int, data: QuizCreate, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    return await quiz_crud.update(db=db, data=data, user_id=current_user.id, id_=id_)

@quiz_router.delete("/delete")
async def delete_quiz(id_: int, current_user = Depends(get_current_user),  db: AsyncSession = Depends(get_db)):
    return await quiz_crud.delete(id_=id_, user_id=current_user.id, db=db)

@quiz_router.get("/get_all_in_specific_company")
async def get_all(company_id: int, db: AsyncSession = Depends(get_db)):
    return await quiz_crud.get_all_by_filter(db=db, filters={"company_id": company_id})

@quiz_router.get("/get_all")
async def get_all(db: AsyncSession = Depends(get_db)):
    return await quiz_crud.get_all(db=db)