from fastapi import APIRouter, Depends

from app.middlewares.auth_middleware import genitoreRegistrato_access
from app.schemas.iscrizione import IscrizioneList
from app.services.public.iscrizione import iscrizioni_genitore

iscrizione_router = APIRouter()


@iscrizione_router.get("/", response_model=IscrizioneList, summary="Leggi le iscrizioni del genitore")
async def read_iscrizioni_genitore(genitore=Depends(genitoreRegistrato_access)):
    """
    Legge le iscrizioni del genitore
    """
    iscrizioni = iscrizioni_genitore(genitore.id)
    if not iscrizioni:
        return {"iscrizioni": []}
    return {"iscrizioni": iscrizioni}
