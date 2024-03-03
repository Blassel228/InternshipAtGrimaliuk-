import asyncio_redis
from config import settings

async def redis_connect():
    redis_conn = asyncio_redis.Connection.create(host=settings.redis_host, port=settings.redis_port)
    #r = redis.Redis(host=settings.redis_host, port=settings.redis_port)
    return redis_conn