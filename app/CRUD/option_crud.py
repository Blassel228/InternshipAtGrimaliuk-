from app.repositories.repository import CrudRepository
from app.db.models.models import OptionModel
class OptionCRUD(CrudRepository):
    pass

option_crud = OptionCRUD(model=OptionModel)