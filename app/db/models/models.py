from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker
import datetime
from sqlalchemy import MetaData, Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base
from config import settings
from sqlalchemy.orm import relationship

metadata = MetaData()
Base = declarative_base(metadata=metadata)
engine = create_async_engine(f'postgresql+asyncpg://{settings.postgresql_user}:{settings.postgresql_password}@{settings.postgresql_host}:{settings.postgresql_port}/{settings.postgresql_database_name}')
session = async_sessionmaker(engine)

class UserModel(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    mail = Column(String, nullable=False, unique=True)
    registration_date = Column(String, default=str(datetime.datetime.now()))
    role = Column(Integer, nullable=False)
    hashed_password = Column(String, nullable=False)
    companies = relationship("CompanyModel", back_populates="members", cascade="all, delete-orphan", uselist=True)

class CompanyModel(Base):
    __tablename__ = "company"
    company_id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey("user.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    registration_date = Column(String, default=str(datetime.datetime.now()))
    visible = Column(Boolean, default=True)
    members = relationship("UserModel", back_populates="companies", uselist=True)

class InvitationModel(Base):
    __tablename__ = "invitation"
    invitation_id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("company.company_id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    owner_id = Column(Integer, ForeignKey("user.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    recipient_id = Column(Integer, ForeignKey("user.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    invitation_text = Column(String)
    registration_date = Column(String, default=str(datetime.datetime.now()))

class RequestModel(Base):
    __tablename__ = "request"
    request_id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("company.company_id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    sender_id = Column(Integer, ForeignKey("user.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    company_name = Column(String, nullable=False)
    request_text = Column(String)
    registration_date = Column(String, default=str(datetime.datetime.now()))