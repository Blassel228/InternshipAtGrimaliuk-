from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker
import datetime
from sqlalchemy import MetaData, Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base
from config import settings
from sqlalchemy import event
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
    companies = relationship("CompanyModel", back_populates="owner", cascade="all, delete-orphan")

class CompanyModel(Base):
    __tablename__ = "company"
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey("user.id", onupdate="CASCADE", ondelete="CASCADE"))
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    registration_date = Column(String, default=str(datetime.datetime.now()))
    visible = Column(Boolean, default=True)
    members = relationship("UserModel", back_populates="companies")

@event.listens_for(UserModel, "before_update")
def update_company_owner_id(mapper, connection, target):
    user_id = target.id
    connection.execute(
        CompanyModel.__table__.update()
        .where(CompanyModel.owner_id == user_id)
        .values(owner_id=user_id))

