from app.repositories.repository import CrudRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.schemas import QuizCreate
from app.db.models.models import QuizModel, QuestionModel, OptionModel
from fastapi import HTTPException
from sqlalchemy import delete
from app.CRUD.company_crud import company_crud
from app.CRUD.admin_crud import admin_crud
from app.CRUD.member_crud import member_crud
from app.CRUD.question_crud import question_crud
from app.CRUD.option_crud import option_crud

class QuizCrud(CrudRepository):
    async def create(self, db: AsyncSession, quiz: QuizCreate):
        db_quiz = QuizModel(
            name=quiz.name,
            description=quiz.description,
            company_id=quiz.company_id
        )
        db.add(db_quiz)
        await db.commit()
        await db.refresh(db_quiz)

        if len(quiz.questions) < 2:
            raise HTTPException(detail="There must be two or more questions", status_code=403)
        for question_data in quiz.questions:
            db_question = QuestionModel(
                text=question_data.text,
                quiz_id=db_quiz.id
            )
            db.add(db_question)
            await db.commit()
            await db.refresh(db_question)
            if len(question_data.options) < 2:
                raise HTTPException(detail="There must be two or more options for every question", status_code=403)

            for option_data in question_data.options:
                db_option = OptionModel(
                    text=option_data.text,
                    is_correct=option_data.is_correct,
                    question_id=db_question.id
                )
                db.add(db_option)
        await db.commit()
        return db_quiz

    async def delete(self, id_: int, user_id: int, db: AsyncSession):
        member = await member_crud.get_one(id_=user_id, db=db)
        if member is not None:
            admin = await admin_crud.get_one(id_=member.id, db=db)
        else:
            admin = None
        quiz = await self.get_one(id_=id_, db=db)
        if quiz is None:
            raise HTTPException(detail="There is no a quiz with such an id", status_code=403)
        company = await company_crud.get_one(id_=quiz.company_id, db=db)
        if member is None or member.company_id != quiz.company_id:
            if company.owner_id != user_id:
                raise HTTPException(detail="You can`t delete quizzes", status_code=403)
        if member is not None:
            if admin is  None:
                raise HTTPException(detail="You can`t delete quizzes", status_code=403)
        stmt = delete(self.model).where(self.model.id == id_)
        await db.execute(stmt)
        await db.commit()
        return quiz

    async def update(self, id_: int, db: AsyncSession, data: QuizCreate, user_id: int):
        quiz = await self.get_one(id_=id_, db=db)
        if quiz is None:
            raise HTTPException(detail="Quiz not found", status_code=404)

        company = await company_crud.get_one(id_=quiz.company_id, db=db)
        if company is None:
            raise HTTPException(detail="Company not found", status_code=404)

        if user_id != company.owner_id:
            admin = await admin_crud.get_one(id_=user_id, db=db)
            if admin is None or admin.company_id != company.id:
                raise HTTPException(detail="You are not authorized to update this quiz", status_code=403)

        quiz.name = data.name
        quiz.description = data.description

        await db.execute(delete(QuestionModel).where(QuestionModel.quiz_id == id_))
        questions = await question_crud.get_all_by_filter(filters={"quiz_id": id_}, db=db)
        for question in questions:
            await option_crud.delete_all_by_filters({"question_id": question.id}, db=db)

        for question_data in data.questions:

            db_question = QuestionModel(
                text=question_data.text,
                quiz_id=quiz.id
            )
            db.add(db_question)
            await db.commit()
            await db.refresh(db_question)

            for option_data in question_data.options:
                db_option = OptionModel(
                    text=option_data.text,
                    is_correct=option_data.is_correct,
                    question_id=db_question.id
                )
                db.add(db_option)

        await db.commit()
        return quiz

quiz_crud = QuizCrud(QuizModel)