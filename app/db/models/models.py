from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import datetime
from sqlalchemy import MetaData, Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base
from config import settings
from app.db.base import Base

class UserModel(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    mail = Column(String, nullable=False, unique=True)
    registration_date = Column(String, default=str(datetime.datetime.now()))
    role = Column(Integer, nullable=False)
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
    id = Column(Integer,ForeignKey("user.id", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True, )
    company_id = Column(Integer, ForeignKey("company.id", onupdate="CASCADE", ondelete="CASCADE"),nullable=False)
    registration_date = Column(String, default=str(datetime.datetime.now()))