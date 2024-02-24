from app.repositories.repository import CrudRepository
from app.db.models.models import MemberModel

class MemberCrud(CrudRepository):
    pass

member_crud = MemberCrud(MemberModel)