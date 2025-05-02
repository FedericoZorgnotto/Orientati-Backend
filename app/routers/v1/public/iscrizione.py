from fastapi import APIRouter, Depends, HTTPException
from websockets.headers import parse_extension_item

from app.database import get_db
from app.middlewares.auth_middleware import genitoreRegistrato_access, admin_access
from app.models import Gruppo, FasciaOraria, Ragazzo, Iscrizione as IscrizioneModel, Percorso
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

    fasciaOraria = db.query(FasciaOraria).filter(FasciaOraria.id == iscrizione_data.fasciaOraria_id).first()
    if not fasciaOraria:
        return HTTPException(status_code=404, detail="FasciaOraria non trovata")

    # controlla se il genitore ha già un'iscrizione per la stessa data e percorso o se ha già un'iscrizione per la stessa fasciaOraria

    iscrizione_esistente = (db.query(IscrizioneModel)
                            .filter(
        IscrizioneModel.genitore_id == genitore.id,
        IscrizioneModel.fasciaOraria_id == iscrizione_data.fasciaOraria_id,
    ).first())
    if not iscrizione_esistente:
        iscrizione_esistente = (db.query(IscrizioneModel)
                               .join(FasciaOraria).join(Percorso)
                               .filter(
            IscrizioneModel.genitore_id == genitore.id,
            # IscrizioneModel.fasciaOraria.data == fasciaOraria.data,
            Percorso.id == fasciaOraria.percorso_id
        ).first())


    print(fasciaOraria)
    print(fasciaOraria.percorso.nome)
    print(iscrizione_esistente)

    if iscrizione_esistente:
        raise HTTPException(
            status_code=400,
            detail=f"Esiste già un'iscrizione per questa data nel percorso selezionato"
        )

    # controlla se i ragazzi esistono nel database
    for ragazzo_id in iscrizione_data.ragazzi_id:
        ragazzo = db.query(Ragazzo).filter(Ragazzo.id == ragazzo_id).first()
        if not ragazzo:
            raise HTTPException(status_code=404, detail=f"Ragazzo con ID {ragazzo_id} non trovato")

    iscrizione = create_iscrizione(
        genitore_id=genitore.id,
        fasciaOraria_id=iscrizione_data.fasciaOraria_id,
        ragazzi_id=iscrizione_data.ragazzi_id
    )
    return iscrizione

# TODO: ridurre dimensione funzione

# TODO: aggiungere endpoint per eliminare iscrizione
# TODO: aggiungere endpoint per modificare iscrizione
