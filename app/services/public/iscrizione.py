from sqlalchemy.orm import joinedload

from app.database import get_db
from app.models import Ragazzo
from app.models.iscrizione import Iscrizione


def iscrizioni_genitore(genitore_id: int):
    """
    Get all the registrations of a parent by their ID.
    """
    database = next(get_db())
    iscrizioni = (
        database.query(Iscrizione)
        .options(joinedload(Iscrizione.ragazzi))
        .filter(Iscrizione.genitore_id == genitore_id)
        .all()
    )
    if not iscrizioni:
        return None
    return iscrizioni


def iscrizioni_all():
    """
    Get all registrations.
    """
    database = next(get_db())
    iscrizioni = (database.query(Iscrizione)
                  .options(joinedload(Iscrizione.ragazzi))
                  .all())
    if not iscrizioni:
        return None
    return iscrizioni


def create_iscrizione(genitore_id: int, gruppo_id: int, fasciaOraria_id: int, ragazzi_id: list[int]):
    """
    Create a new registration for a parent.
    """
    database = next(get_db())
    iscrizione = Iscrizione(
        genitore_id=genitore_id,
        gruppo_id=gruppo_id,
        fasciaOraria_id=fasciaOraria_id
    )

    ragazzi = database.query(Ragazzo).filter(Ragazzo.id.in_(ragazzi_id)).all()
    iscrizione.ragazzi = ragazzi

    database.add(iscrizione)
    database.commit()
    database.refresh(iscrizione)
    iscrizione.ragazzi = ragazzi
    return iscrizione
