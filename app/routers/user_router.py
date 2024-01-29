from typing import Annotated
from fastapi import APIRouter, Depends
from app.db.models.models import get_db
from sqlalchemy.orm import Session
from app.schemas.schemas import UserUpdate
from app.services.user_service import user_service
from app.core.autho import oauth2_scheme

user_router = APIRouter(tags=["user"])

@user_router.put("/self_update")
def user_self_update(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db), data: UserUpdate = None):
    return user_service.self_update(token=token, data=data, db=db)

@user_router.delete("/self_delete")
def user_self_delete(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    return user_service.self_delete(token=token, db=db)
