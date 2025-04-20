from fastapi import APIRouter

from app.schemas.scuolaDiProvenienza import ScuolaDiProvenienzaList
from app.services.scuolaDiProvenienza import get_all_ufficiali

scuola_router = APIRouter()


@scuola_router.get("/", response_model=ScuolaDiProvenienzaList, summary="Leggi scuole di provenienza")
async def get_all():
    """
    Legge tutte le scuole di provenienza, escluse quelle create dai ragazzi
    """
    return ScuolaDiProvenienzaList(scuole=get_all_ufficiali())
