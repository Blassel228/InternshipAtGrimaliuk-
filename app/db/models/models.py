from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker
import datetime
from sqlalchemy import MetaData, Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from config import settings

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

    def __init__(self, id, username, mail, role, hashed_password):
        self.id=id
        self.username=username
        self.mail=mail
        self.role=role
        self.hashed_password=hashed_password

async def get_db():
    db = session()
    try:
        yield db
    finally:
        await db.close()