from fastapi import APIRouter

from app.schemas.public.genitore import GenitoreLogin
from app.services.public.genitore import login as login_genitore

genitore_router = APIRouter()


@genitore_router.post("/", response_model=GenitoreLogin)
async def login(email: str):
    """
    Effettua il login di un genitore tramite email
    """
    return login_genitore(email)
    # return GenitoreLogin(
    #     access_token="token",
    #     token_type="bearer",
    #     email=email,
    #     nome="Nome",
    #     cognome="Cognome",
    #     comune="Comune",
    #     id=1,
    # )