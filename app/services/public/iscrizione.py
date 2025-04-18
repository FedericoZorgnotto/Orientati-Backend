from app.database import get_db
from app.models.iscrizione import Iscrizione


def iscrizioni_genitore(genitore_id: int):
    """
    Get all the registrations of a parent by their ID.
    """
    database = next(get_db())
    iscrizioni = database.query(Iscrizione).filter(Iscrizione.genitore_id == genitore_id).all()
    if not iscrizioni:
        return None
    return iscrizioni
