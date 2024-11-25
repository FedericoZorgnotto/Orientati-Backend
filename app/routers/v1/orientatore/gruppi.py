import datetime

import pytz
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models import Utente, Gruppo
from app.schemas.OrientatoreSchema.tappa import TappaList, TappaResponse
from app.schemas.gruppo import GruppoList

gruppo_router = APIRouter()


@gruppo_router.get("/", response_model=GruppoList)
async def get_gruppi_orientatore_utente(db: Session = Depends(get_db),
                                        current_user: Utente = Depends(get_current_user)):
    """
    restituisce i gruppi ai quali l'utente è connesso tramite l'orientatore
    """

    if current_user.orientatore_id is None:
        raise HTTPException(status_code=404, detail="Utente non associato ad un orientatore")

    if current_user.orientatore.gruppi is []:
        raise HTTPException(status_code=404, detail="Orientatore non associato ad un gruppo")
    GruppoList.gruppi = current_user.orientatore.gruppi
    for gruppo in GruppoList.gruppi:
        if gruppo.numero_tappa == 0 and gruppo.arrivato is True:
            GruppoList.gruppi.remove(gruppo)

    return GruppoList


@gruppo_router.get("/tappe/{gruppo_id}", response_model=TappaList)
async def get_tappe_gruppo(gruppo_id: int, db: Session = Depends(get_db),
                           current_user: Utente = Depends(get_current_user)):
    """
    restituisce le tappe del gruppo
    """

    gruppo = db.query(Gruppo).filter(Gruppo.id == gruppo_id).first()

    if not gruppo:
        raise HTTPException(status_code=404, detail="Gruppo not found")

    if current_user.orientatore is None:
        raise HTTPException(status_code=404, detail="Utente non associato ad un orientatore")

    if current_user.orientatore.gruppi is None:
        raise HTTPException(status_code=404, detail="Orientatore non associato ad un gruppo")

    if gruppo not in current_user.orientatore.gruppi:
        raise HTTPException(status_code=403, detail="Utente non autorizzato")
    # TappaList.tappe = sorted(gruppo.percorso.tappe, key=lambda tappa: tappa.minuti_arrivo)
    TappaList.tappe = []

    for tappa in gruppo.percorso.tappe:
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

    return TappaList


@gruppo_router.get("/tappa/{gruppo_id}/{numero_tappa}", response_model=TappaResponse)
async def get_tappa_gruppo(gruppo_id: int, numero_tappa: int, db: Session = Depends(get_db),
                           current_user: Utente = Depends(get_current_user)):
    """
    restituisce la tappa N del gruppo
    """

    gruppo = db.query(Gruppo).filter(Gruppo.id == gruppo_id).first()

    if not gruppo:
        raise HTTPException(status_code=404, detail="Gruppo not found")

    if current_user.orientatore is None:
        raise HTTPException(status_code=404, detail="Utente non associato ad un orientatore")

    if current_user.orientatore.gruppi is None:
        raise HTTPException(status_code=404, detail="Orientatore non associato ad un gruppo")

    if gruppo not in current_user.orientatore.gruppi:
        raise HTTPException(status_code=403, detail="Utente non autorizzato")

    tappe = sorted(gruppo.percorso.tappe, key=lambda tappa: tappa.minuti_arrivo)
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

    gruppo = db.query(Gruppo).filter(Gruppo.id == gruppo_id).first()

    if not gruppo:
        raise HTTPException(status_code=404, detail="Gruppo not found")

    if current_user.orientatore is None:
        raise HTTPException(status_code=404, detail="Utente non associato ad un orientatore")

    if current_user.orientatore.gruppi is None:
        raise HTTPException(status_code=404, detail="Orientatore non associato ad un gruppo")

    if gruppo not in current_user.orientatore.gruppi:
        raise HTTPException(status_code=403, detail="Utente non autorizzato")

    if tappa < 0 or tappa > len(gruppo.percorso.tappe):
        raise HTTPException(status_code=404, detail="Tappa non trovata")

    if tappa == 1 and arrivato is False:
        gruppo.orario_partenza_effettivo = datetime.datetime.now(pytz.timezone("Europe/Rome")).strftime("%H:%M")

    if tappa == 0 and arrivato is True:
        gruppo.orario_fine_effettivo = datetime.datetime.now(pytz.timezone("Europe/Rome")).strftime("%H:%M")

    gruppo.numero_tappa = tappa
    gruppo.arrivato = arrivato
    db.commit()
    db.refresh(gruppo)

    return gruppo
