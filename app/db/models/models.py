import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base
from config import settings
from sqlalchemy.orm import relationship

metadata = MetaData()
Base = declarative_base(metadata=metadata)
engine = create_async_engine(f'postgresql+asyncpg://{settings.postgresql_user}:{settings.postgresql_password}@{settings.postgresql_host}:{settings.postgresql_port}/{settings.postgresql_database_name}')
session = async_sessionmaker(engine, expire_on_commit=False)
class UserModel(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    mail = Column(String, nullable=False, unique=True)
    registration_date = Column(String, default=str(datetime.datetime.now()))
    hashed_password = Column(String, nullable=False)

class CompanyModel(Base):
    __tablename__ = "company"
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey("user.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    registration_date = Column(String, default=str(datetime.datetime.now()))
    visible = Column(Boolean, default=True)

class InvitationModel(Base):
    __tablename__ = "invitation"
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("company.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    owner_id = Column(Integer, ForeignKey("user.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    recipient_id = Column(Integer, ForeignKey("user.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    registration_date = Column(String, default=str(datetime.datetime.now()))
    invitation_text = Column(String)

class RequestModel(Base):
    __tablename__ = "request"
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("company.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    sender_id = Column(Integer, ForeignKey("user.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    registration_date = Column(String, default=str(datetime.datetime.now()))
    request_text = Column(String)

class MemberModel(Base):
    __tablename__ = "member"
    id = Column(Integer,ForeignKey("user.id", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
    company_id = Column(Integer, ForeignKey("company.id", onupdate="CASCADE", ondelete="CASCADE"),nullable=False)
    registration_date = Column(String, default=str(datetime.datetime.now()))

class AdminModel(Base):
    __tablename__ = "admin"
    id = Column(Integer, ForeignKey("member.id", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
    registration_date = Column(String, default=str(datetime.datetime.now()))

class QuizModel(Base):
    __tablename__ = "quiz"
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("company.id", onupdate="CASCADE", ondelete="CASCADE"))
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    questions = relationship("QuestionModel", back_populates="quizzes", cascade="all, delete-orphan")
    registration_date = Column(String, default=str(datetime.datetime.now()))

    def __init__(self, name: str, description: str, company_id: int):
        self.name = name
        self.description = description
        self.company_id = company_id

class QuestionModel(Base):
    __tablename__ = 'question'
    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    quiz_id = Column(Integer, ForeignKey('quiz.id',  onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    options = relationship("OptionModel", back_populates="question", cascade="all, delete-orphan")
    quizzes = relationship("QuizModel", back_populates="questions")

    def __init__(self, text: str, quiz_id: int):
        self.text = text
        self.quiz_id = quiz_id

class OptionModel(Base):
    __tablename__ = 'option'
    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    is_correct = Column(Boolean, nullable=False, default=False)
    question_id = Column(Integer, ForeignKey('question.id',onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    question = relationship("QuestionModel", back_populates="options")

    def __init__(self, text: str, is_correct: bool, question_id: int):
        self.text = text
        self.is_correct = is_correct
        self.question_id = question_id