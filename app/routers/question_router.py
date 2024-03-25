from app.CRUD.question_crud import question_crud
from app.schemas.schemas import QuestionCreate
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, APIRouter
from app.utils.deps import get_db
from app.utils.deps import get_current_user

question_crud = APIRouter(tags=["/question"])

@question_crud.post("/create")
def create_quiz(question: QuestionCreate, db: AsyncSession = Depends(get_db)):
    return question_crud.create(db=db, question=question)

