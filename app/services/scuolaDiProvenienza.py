from app.database import get_db
from app.models import ScuolaDiProvenienza


def get_all_ufficiali():
    """
    Restituisce la lista delle scuole ufficiali
    """
    database = next(get_db())
    scuole = database.query(ScuolaDiProvenienza).filter(ScuolaDiProvenienza.isUfficiale.is_(True)).all()
    return scuole
