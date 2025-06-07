from app.database import get_db
from app.models import Genitore
from app.schemas.email import SendEmailSchema
from app.schemas.genitore import GenitoreLogin
from app.services.auth import generate_genitore_access_token
from app.services.email import Mailer


async def login(email):
    database = next(get_db())
    genitore = database.query(Genitore).filter(Genitore.email == email).first()
    if not genitore:
        genitore = Genitore(email=email)
        database.add(genitore)
        database.commit()
        database.refresh(genitore)
        genitore = database.query(Genitore).filter(Genitore.email == email).first()
        await inviaEmail(genitore)

    # genera il token
    token = generate_genitore_access_token(genitore)
    return GenitoreLogin(
        access_token=token,
        token_type="bearer",
        email=str(genitore.email),
        nome=genitore.nome or "",
        cognome=genitore.cognome or "",
        comune=genitore.comune or "",
        id=genitore.id,
    )


def update(email: str, nome: str, cognome: str, comune: str):
    database = next(get_db())
    genitore = database.query(Genitore).filter(Genitore.email == email).first()
    if not genitore:
        return None
    genitore.nome = nome
    genitore.cognome = cognome
    genitore.comune = comune
    database.commit()
    database.refresh(genitore)
    return genitore


async def inviaEmail(genitore: Genitore):
    """
    Invia un'email al genitore per confermare la registrazione
    """
    email_schema = SendEmailSchema(
        subject="Benvenuto",
        recipient=genitore.email,
        template_name="welcome.html"
    )
    mailer = Mailer()
    await mailer.send_template(email_schema)
