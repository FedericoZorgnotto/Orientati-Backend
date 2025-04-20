from fastapi import APIRouter, Depends

from app.middlewares.auth_middleware import genitore_access
from app.schemas.genitore import GenitoreLogin, Genitore, EmailSchema, GenitoreUpdate
from app.services.public.genitore import login as login_genitore, update as update_genitore

genitore_router = APIRouter()


@genitore_router.get("/", response_model=Genitore, summary="Leggi informazioni genitore")
async def read_genitore(genitore=Depends(genitore_access)):
    """
    Legge le informazioni del genitore
    """
    return genitore


@genitore_router.post("/", response_model=GenitoreLogin, summary="Login genitore")
async def login(email_data: EmailSchema):
    """
    Effettua il login di un genitore tramite email nel body della richiesta
    """
    return login_genitore(email_data.email)


@genitore_router.put("/", response_model=Genitore, summary="Aggiorna genitore dopo login iniziale")
async def update(genitore_data: GenitoreUpdate, _=Depends(genitore_access)):
    """
    Aggiorna le informazioni del genitore
    """
    return update_genitore(**genitore_data.model_dump())
