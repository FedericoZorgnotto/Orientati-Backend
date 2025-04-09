from app.database import get_db
from app.models import Genitore
from app.schemas.public.genitore import GenitoreLogin
from app.services.auth import generate_genitore_access_token


def login(email):
    database = next(get_db())
    genitore = database.query(Genitore).filter(Genitore.email == email).first()
    if not genitore:
        genitore = Genitore(email=email)
        database.add(genitore)
        database.commit()
        database.refresh(genitore)
        genitore = database.query(Genitore).filter(Genitore.email == email).first()

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
