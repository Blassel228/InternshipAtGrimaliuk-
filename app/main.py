import uvicorn
from fastapi import FastAPI
from config import settings
from app.routers.user import user_router
from fastapi_pagination import add_pagination

app = FastAPI()
app.include_router(user_router, prefix="/user")
@app.get("/")
def read_root():
    return {"status_code": 200, "detail": "ok", "result": "working"}

@app.get("/health_check")
def health_check():
    return {"status_code": 200, "detail": "ok", "result": "healthy"}

add_pagination(app)

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.host, port=settings.port, reload=True)