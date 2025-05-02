from sqlalchemy.orm import joinedload

from app.database import get_db
from app.models import Ragazzo, Genitore
from app.models.iscrizione import Iscrizione
from app.schemas.email import SendEmailSchema
from app.services.email import Mailer


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


async def create_iscrizione(genitore_id: int, fasciaOraria_id: int, ragazzi_id: list[int]):
    """
    Create a new registration for a parent.
    """
    database = next(get_db())
    iscrizione = Iscrizione(
        genitore_id=genitore_id,
        fasciaOraria_id=fasciaOraria_id
    )

    ragazzi = database.query(Ragazzo).filter(Ragazzo.id.in_(ragazzi_id)).all()
    iscrizione.ragazzi = ragazzi

    database.add(iscrizione)
    database.commit()
    database.refresh(iscrizione)
    iscrizione.ragazzi = ragazzi

    genitore = database.query(Genitore).filter(Genitore.id == genitore_id).first()
    email_schema = SendEmailSchema(
        subject="Conferma Iscrizione",
        recipient=genitore.email,
        template_name="conferma_iscrizione.html",
        context={
            "percorso": iscrizione.fasciaOraria.percorso.nome,
            "ora": iscrizione.fasciaOraria.oraInizio,
            "data": iscrizione.fasciaOraria.data.data.strftime("%d/%m/%Y"),
        }
    )
    mailer = Mailer()
    await mailer.send_template(email_schema)

    return iscrizione


def delete_iscrizione(iscrizione_id: int):
    """
    Delete a registration by its ID.
    """
    database = next(get_db())
    iscrizione = database.query(Iscrizione).filter(Iscrizione.id == iscrizione_id).first()
    if not iscrizione:
        return None
    database.delete(iscrizione)
    database.commit()
    return iscrizione


def update_iscrizione(
        iscrizione_id: int,
        fasciaOraria_id: int,
        ragazzi_id: list[int]
):
    """
    Update a registration by its ID.
    """
    database = next(get_db())
    iscrizione = database.query(Iscrizione).filter(Iscrizione.id == iscrizione_id).first()
    if not iscrizione:
        return None

    iscrizione.fasciaOraria_id = fasciaOraria_id
    iscrizione.ragazzi = database.query(Ragazzo).filter(Ragazzo.id.in_(ragazzi_id)).all()

    database.commit()
    database.refresh(iscrizione)
    return iscrizione
