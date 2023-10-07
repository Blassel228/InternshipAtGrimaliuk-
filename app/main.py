import uvicorn
from fastapi import FastAPI
from config import settings
from databases import Database
import asyncio_redis
import redis

app = FastAPI()

async def redis_connect():
    redis_conn = asyncio_redis.Connection.create(host=settings.redis_host, port=settings.redis_port)
    #r = redis.Redis(host=settings.redis_host, port=settings.redis_port)
    return redis_conn

async def postgresql_connection():
    postgres_conn = Database(f'postgresql://{settings.postgresql_user}:{settings.postgresql_password}'
                             f'@{settings.postgresql_host}:{settings.postgresql_port}/{settings.postgresql_database_name}')
    await postgres_conn.connect()
    return postgres_conn

@app.get("/")
def read_root():
    return {"status_code": 200, "detail": "ok", "result": "working"}

@app.get("/health_check")
def health_check():
    return {"status_code": 200, "detail": "ok", "result": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.host, port=settings.port, reload=True)