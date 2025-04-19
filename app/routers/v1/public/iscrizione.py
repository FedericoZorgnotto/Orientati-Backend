from fastapi import APIRouter, Depends, HTTPException

from app.database import get_db
from app.middlewares.auth_middleware import genitoreRegistrato_access, admin_access
from app.models import Gruppo, FasciaOraria, Ragazzo
from app.schemas.iscrizione import IscrizioneList, Iscrizione, IscrizioneCreate
from app.services.public.iscrizione import iscrizioni_genitore, iscrizioni_all, create_iscrizione

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


@iscrizione_router.get("/all", response_model=IscrizioneList, summary="Leggi tutte le iscrizioni")
async def read_all_iscrizioni(admin=Depends(admin_access)):
    """
    Legge tutte le iscrizioni (solo amministratori)
    """
    iscrizioni = iscrizioni_all()
    if not iscrizioni:
        return {"iscrizioni": []}
    return {"iscrizioni": iscrizioni}


@iscrizione_router.post("/", response_model=Iscrizione, summary="Crea una nuova iscrizione")
async def create_iscrizione_endpoint(
        iscrizione_data: IscrizioneCreate,
        genitore=Depends(genitoreRegistrato_access),
        db=Depends(get_db)
):
    """
    Crea una nuova iscrizione per il genitore autenticato
    """
    # controlla se gruppo e fasciaOraria esistono nel database
    gruppo = db.query(Gruppo).filter(Gruppo.id == iscrizione_data.gruppo_id).first()
    if not gruppo:
        raise HTTPException(status_code=404, detail="Gruppo non trovato")
    fasciaOraria = db.query(FasciaOraria).filter(FasciaOraria.id == iscrizione_data.fasciaOraria_id).first()
    if not fasciaOraria:
        return HTTPException(status_code=404, detail="FasciaOraria non trovata")

    # controlla se i ragazzi esistono nel database
    for ragazzo_id in iscrizione_data.ragazzi_id:
        ragazzo = db.query(Ragazzo).filter(Ragazzo.id == ragazzo_id).first()
        if not ragazzo:
            raise HTTPException(status_code=404, detail=f"Ragazzo con ID {ragazzo_id} non trovato")

    iscrizione = create_iscrizione(
        genitore_id=genitore.id,
        gruppo_id=iscrizione_data.gruppo_id,
        fasciaOraria_id=iscrizione_data.fasciaOraria_id,
        ragazzi_id=iscrizione_data.ragazzi_id
    )
    return iscrizione
