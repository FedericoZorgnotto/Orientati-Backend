import datetime

import pytz
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models import Utente, Percorso, Gruppo, Tappa
from app.schemas.OrientatoreSchema.gruppo import GruppoResponse, GruppoResponsePresenze
from app.schemas.OrientatoreSchema.tappa import TappaList, TappaResponse

gruppo_router = APIRouter()


@gruppo_router.get("/", response_model=GruppoResponsePresenze)
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
    gruppoPresenze: GruppoResponsePresenze = GruppoResponsePresenze(
        id=gruppo.id,
        nome=gruppo.nome,
        data=gruppo.data,
        orario_partenza=gruppo.orario_partenza,
        percorso_id=gruppo.percorso_id,
        numero_tappa=gruppo.numero_tappa,
        arrivato=gruppo.arrivato,
        percorso_finito=gruppo.percorso_finito
    )
    gruppoPresenze.orientati_presenti = db.query(Utente).filter(Utente.gruppo_id == current_user.gruppo_id).count()
    gruppoPresenze.orientati_assenti = db.query(Utente).filter(Utente.gruppo_id == current_user.gruppo_id).count()
    gruppoPresenze.orientati_totali = db.query(Utente).filter(Utente.gruppo_id == current_user.gruppo_id).count()
    return gruppoPresenze


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

    Lista = TappaList(tappe=[])

    for tappa in sorted(current_user.gruppo.percorso.tappe, key=lambda tappa: tappa.minuti_arrivo):
        Lista.tappe.append(TappaResponse(
            id=tappa.id,
            percorso_id=tappa.percorso.id,
            aula_id=tappa.aula.id,
            minuti_arrivo=tappa.minuti_arrivo,
            minuti_partenza=tappa.minuti_partenza,
            aula_nome=tappa.aula.nome,
            aula_posizione=tappa.aula.posizione,
            aula_materia=tappa.aula.materia,
        ))

    return Lista


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

    occupata = False
    percorsi = db.query(Percorso).filter(Percorso.id == tappa.percorso_id).all()
    for percorso in percorsi:
        gruppi = db.query(Gruppo).filter(Gruppo.percorso_id == percorso.id).all()
        for gruppo in gruppi:
            tappe = db.query(Tappa).order_by(Tappa.minuti_partenza).filter(
                Tappa.percorso_id == percorso.id).all()
            if (tappe[gruppo.numero_tappa - 1].aula_id == tappa.aula_id
                    and gruppo.arrivato is True and not gruppo.numero_tappa == 0):
                occupata = True
                break

    tappa.occupata = occupata

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
        current_user.gruppo.orario_partenza_effettivo = datetime.datetime.now(pytz.timezone("Europe/Rome")).strftime(
            "%H:%M")

    if tappa == 0 and arrivato is True:
        current_user.gruppo.orario_fine_effettivo = datetime.datetime.now(pytz.timezone("Europe/Rome")).strftime(
            "%H:%M")

    current_user.gruppo.numero_tappa = tappa
    current_user.gruppo.arrivato = arrivato
    current_user.gruppo.numero_tappa = tappa
    current_user.gruppo.arrivato = arrivato
    db.commit()
    db.refresh(current_user)

    return current_user.gruppo
