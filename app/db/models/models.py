import datetime
from sqlalchemy import MetaData, Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from config import settings

metadata = MetaData()
Base = declarative_base(metadata=metadata)
engine = create_engine(f'postgresql://{settings.postgresql_user}:{settings.postgresql_password}@{settings.postgresql_host}:{settings.postgresql_port}/{settings.postgresql_database_name}')
session = sessionmaker(engine)

class UserModel(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    mail = Column(String, nullable=False)
    registration_date = Column(String, default=datetime.datetime.now())
    role = Column(Integer, nullable=False)
    hashed_password = Column(String, nullable=False)

async def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()