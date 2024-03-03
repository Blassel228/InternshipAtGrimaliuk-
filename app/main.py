import uvicorn
from fastapi import FastAPI
from config import settings
from app.routers.user_router import user_router
from app.routers.token_router import token_router
from app.routers.invitation_router import invitation_router
from app.routers.request_router import request_router
from app.routers.member_router import member_router
from app.routers.company_router import company_router
from app.routers.admin_router import admin_router
from fastapi_pagination import add_pagination

app = FastAPI()
app.include_router(user_router)
app.include_router(token_router)
app.include_router(company_router)
app.include_router(invitation_router)
app.include_router(request_router)
app.include_router(member_router)
app.include_router(admin_router)
@app.get("/")
def read_root():
    return {"status_code": 200, "detail": "ok", "result": "working"}

@app.get("/health_check")
def health_check():
    return {"status_code": 200, "detail": "ok", "result": "healthy"}

add_pagination(app)

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.host, port=settings.port, reload=True)