from fastapi import APIRouter, Depends, HTTPException
from websockets.headers import parse_extension_item

from app.database import get_db
from app.middlewares.auth_middleware import genitoreRegistrato_access, admin_access
from app.models import Gruppo, FasciaOraria, Ragazzo, Iscrizione as IscrizioneModel, Percorso
from app.schemas.iscrizione import IscrizioneList, Iscrizione, IscrizioneCreate, IscrizioneUpdate
from app.services.public.iscrizione import iscrizioni_genitore, iscrizioni_all, create_iscrizione, delete_iscrizione, \
    update_iscrizione

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

    iscrizione = await create_iscrizione(
        genitore_id=genitore.id,
        fasciaOraria_id=iscrizione_data.fasciaOraria_id,
        ragazzi_id=iscrizione_data.ragazzi_id
    )
    return iscrizione


@iscrizione_router.delete("/{iscrizione_id}", response_model=Iscrizione, summary="Elimina iscrizione")
async def delete_iscrizione_endpoint(
        iscrizione_id: int,
        genitore=Depends(genitoreRegistrato_access),
        db=Depends(get_db)
):
    """
    Elimina un'iscrizione per il genitore autenticato
    """
    # controlla se l'iscrizione esiste nel database
    iscrizione = db.query(IscrizioneModel).filter(IscrizioneModel.id == iscrizione_id).first()
    if not iscrizione:
        raise HTTPException(status_code=404, detail="Iscrizione non trovata")

    # controlla se l'iscrizione appartiene al genitore
    if iscrizione.genitore_id != genitore.id:
        raise HTTPException(status_code=403, detail="Non hai i permessi per eliminare questa iscrizione")

    delete_iscrizione(iscrizione_id)

    return iscrizione


@iscrizione_router.put("/{iscrizione_id}", response_model=Iscrizione, summary="Modifica iscrizione")
async def update_iscrizione_endpoint(
        iscrizione_id: int,
        iscrizione_data: IscrizioneUpdate,
        genitore=Depends(genitoreRegistrato_access),
        db=Depends(get_db)
):
    """
    Modifica un'iscrizione per il genitore autenticato
    """
    # controlla se l'iscrizione esiste nel database
    iscrizione = db.query(IscrizioneModel).filter(IscrizioneModel.id == iscrizione_id).first()
    if not iscrizione:
        raise HTTPException(status_code=404, detail="Iscrizione non trovata")

    # controlla se l'iscrizione appartiene al genitore
    if iscrizione.genitore_id != genitore.id:
        raise HTTPException(status_code=403, detail="Non hai i permessi per modificare questa iscrizione")

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
            Percorso.id == iscrizione_data.fasciaOraria_id
        ).first())
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
    # aggiorna l'iscrizione
    return update_iscrizione(
        iscrizione_id=iscrizione_id,
        fasciaOraria_id=iscrizione_data.fasciaOraria_id,
        ragazzi_id=iscrizione_data.ragazzi_id
    )

# TODO: ridurre dimensione funzioni
