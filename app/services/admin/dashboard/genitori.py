from app.database import get_db_context
from app.models import Genitore


def get_all_genitori():
    with get_db_context() as db:
        genitori = db.query(Genitore).distinct().all()
        genitori_list = [genitore for genitore in genitori if genitore is not None]
        return genitori_list
