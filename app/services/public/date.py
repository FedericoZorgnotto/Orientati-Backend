from sqlalchemy.orm import joinedload

from app.database import get_db
from app.models.data import Data
from app.models.fasciaOraria import FasciaOraria


def get_all_date():
    """
    Restituisce tutte le date con opzione per includere le fasce orarie
    :return: Lista di oggetti Data
    """
    database = next(get_db())
    date = database.query(Data).options(joinedload(Data.fasceOrarie).subqueryload(FasciaOraria.percorso)).all()
    return date
