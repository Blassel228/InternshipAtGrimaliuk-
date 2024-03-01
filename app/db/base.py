import asyncio_redis
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base
from config import settings

metadata = MetaData()
Base = declarative_base(metadata=metadata)
engine = create_async_engine(f'postgresql+asyncpg://{settings.postgresql_user}:{settings.postgresql_password}@{settings.postgresql_host}:{settings.postgresql_port}/{settings.postgresql_database_name}')
session = async_sessionmaker(engine, expire_on_commit=False)
async def redis_connect():
    redis_conn = asyncio_redis.Connection.create(host=settings.redis_host, port=settings.redis_port)
    #r = redis.Redis(host=settings.redis_host, port=settings.redis_port)
    return redis_conn