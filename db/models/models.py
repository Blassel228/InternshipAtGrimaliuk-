import datetime
from sqlalchemy import MetaData, Column, TIMESTAMP, Integer, String#, create_engine
from sqlalchemy.orm import declarative_base#, sessionmaker
#from config import settings

metadata = MetaData()
Base = declarative_base(metadata=metadata)
class UserModel(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    mail = Column(String, nullable=False)
    registration_date = Column(TIMESTAMP, default=datetime.UTC)
    role = Column(Integer, nullable=False)



