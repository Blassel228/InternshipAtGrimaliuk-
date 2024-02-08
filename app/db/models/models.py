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

    def __init__(self, id, username, mail, role, hashed_password):
        self.id=id
        self.username=username
        self.mail=mail
        self.role=role
        self.hashed_password=hashed_password

class CompanyModel(Base):
    __tablename__ = "company"
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey("user.id", onupdate="CASCADE", ondelete="CASCADE"))
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    registration_date = Column(String, default=str(datetime.datetime.now()))
    visible = Column(Boolean, default=True)
    owner = relationship("UserModel", back_populates="companies")

    def __init__(self, owner_id, name, description):
        self.owner_id = owner_id
        self.name = name
        self.description = description

@event.listens_for(UserModel, "before_update")
def update_company_owner_id(mapper, connection, target):
    user_id = target.id
    connection.execute(
        CompanyModel.__table__.update()
        .where(CompanyModel.owner_id == user_id)
        .values(owner_id=user_id))

async def get_db():
    db = session()
    try:
        yield db
    finally:
        await db.close()