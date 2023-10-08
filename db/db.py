# TODO: rename file into base.py

from databases import Database
import asyncio_redis
from config import settings
import redis

async def redis_connect():
    redis_conn = asyncio_redis.Connection.create(host=settings.redis_host, port=settings.redis_port)
    #r = redis.Redis(host=settings.redis_host, port=settings.redis_port)
    return redis_conn

async def postgresql_connection():
    postgres_conn = Database(f'postgresql://{settings.postgresql_user}:{settings.postgresql_password}'
                             f'@{settings.postgresql_host}:{settings.postgresql_port}/{settings.postgresql_database_name}')
    await postgres_conn.connect()
    return postgres_conn
