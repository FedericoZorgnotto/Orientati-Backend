import datetime

import pytz
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models import Utente
from app.schemas.OrientatoreSchema.tappa import TappaList, TappaResponse
from app.schemas.OrientatoreSchema.gruppo import GruppoResponse

gruppo_router = APIRouter()


@gruppo_router.get("/", response_model=GruppoResponse)
async def get_gruppo_utente(db: Session = Depends(get_db),
                            current_user: Utente = Depends(get_current_user)):
    """
    restituisce il gruppo al quale l'utente è connesso
    """

    if current_user.gruppo_id is None:
        raise HTTPException(status_code=404, detail="Utente non associato ad un gruppo")

    gruppo: GruppoResponse = GruppoResponse.model_validate(current_user.gruppo)
    if gruppo.numero_tappa == 0 and gruppo.arrivato:
        gruppo.percorso_finito = True
    return gruppo


@gruppo_router.get("/tappe/{gruppo_id}", response_model=TappaList)
async def get_tappe_gruppo(gruppo_id: int, db: Session = Depends(get_db),
                           current_user: Utente = Depends(get_current_user)):
    """
    restituisce le tappe del gruppo
    """

    if current_user.gruppo is None:
        raise HTTPException(status_code=404, detail="Utente non associato ad un gruppo")

    if gruppo_id != current_user.gruppo_id:
        raise HTTPException(status_code=403, detail="Utente non autorizzato")

    TappaList.tappe = []

    for tappa in current_user.gruppo.percorso.tappe:
        TappaList.tappe.append(TappaResponse(
            id=tappa.id,
            percorso_id=tappa.percorso.id,
            aula_id=tappa.aula.id,
            minuti_arrivo=tappa.minuti_arrivo,
            minuti_partenza=tappa.minuti_partenza,
            aula_nome=tappa.aula.nome,
            aula_posizione=tappa.aula.posizione,
            aula_materia=tappa.aula.materia,
        ))

    TappaList.tappe = sorted(current_user.gruppo.percorso.tappe, key=lambda tappa: tappa.minuti_partenza)

    return TappaList


@gruppo_router.get("/tappa/{gruppo_id}/{numero_tappa}", response_model=TappaResponse)
async def get_tappa_gruppo(gruppo_id: int, numero_tappa: int, db: Session = Depends(get_db),
                           current_user: Utente = Depends(get_current_user)):
    """
    restituisce la tappa N del gruppo
    """

    if current_user.gruppo is None:
        raise HTTPException(status_code=404, detail="Utente non associato ad un gruppo")

    if gruppo_id != current_user.gruppo_id:
        raise HTTPException(status_code=403, detail="Utente non autorizzato")

    tappe = sorted(current_user.gruppo.percorso.tappe, key=lambda tappa: tappa.minuti_arrivo)
    if numero_tappa <= 0 or numero_tappa > len(tappe):
        raise HTTPException(status_code=404, detail="Tappa non trovata")

    numero_tappa = numero_tappa - 1

    tappa: TappaResponse = tappe[numero_tappa]
    tappa.aula_nome = tappe[numero_tappa].aula.nome
    tappa.aula_posizione = tappe[numero_tappa].aula.posizione
    tappa.aula_materia = tappe[numero_tappa].aula.materia
    return tappa


@gruppo_router.put("/imposta_tappa/{gruppo_id}")
async def imposta_tappa_gruppo(gruppo_id: int, tappa: int, arrivato: bool, db: Session = Depends(get_db),
                               current_user: Utente = Depends(get_current_user)):
    """
    imposta la tappa del gruppo
    """

    if current_user.gruppo is None:
        raise HTTPException(status_code=404, detail="Utente non associato ad un gruppo")

    if gruppo_id != current_user.gruppo_id:
        raise HTTPException(status_code=403, detail="Utente non autorizzato")

    if tappa < 0 or tappa > len(current_user.gruppo.percorso.tappe):
        raise HTTPException(status_code=404, detail="Tappa non trovata")

    if tappa == 1 and arrivato is False:
        current_user.gruppo.orario_partenza_effettivo = datetime.datetime.now(pytz.timezone("Europe/Rome")).strftime("%H:%M")

    if tappa == 0 and arrivato is True:
        current_user.gruppo.orario_fine_effettivo = datetime.datetime.now(pytz.timezone("Europe/Rome")).strftime("%H:%M")

    current_user.gruppo.numero_tappa = tappa
    current_user.gruppo.arrivato = arrivato
    current_user.gruppo.numero_tappa = tappa
    current_user.gruppo.arrivato = arrivato
    db.commit()
    db.refresh(current_user)

    return current_user.gruppo
