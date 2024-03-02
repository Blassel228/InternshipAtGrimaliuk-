from app.db.models.models import UserModel
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from sqlalchemy import insert, update, select
from app.repositories.repository import CrudRepository
from app.schemas.schemas import User
from sqlalchemy.ext.asyncio import AsyncSession

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AdminRepository(CrudRepository):
    pass

admin_crud = AdminRepository(UserModel)