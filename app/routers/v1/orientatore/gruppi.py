from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models import Utente, Gruppo
from app.schemas.gruppo import GruppoList
from app.schemas.tappa import TappaList

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

    if gruppo not in current_user.orientatore.gruppi:
        raise HTTPException(status_code=403, detail="Utente non autorizzato")
    TappaList.tappe = sorted(gruppo.percorso.tappe, key=lambda tappa: tappa.minuti_arrivo)
    return TappaList


@gruppo_router.get("/tappa/{gruppo_id}/{numero_tappa}")
async def get_tappa_gruppo(gruppo_id: int, numero_tappa: int, db: Session = Depends(get_db),
                           current_user: Utente = Depends(get_current_user)):
    """
    restituisce la tappa N del gruppo
    """

    gruppo = db.query(Gruppo).filter(Gruppo.id == gruppo_id).first()

    if not gruppo:
        raise HTTPException(status_code=404, detail="Gruppo not found")

    if gruppo not in current_user.orientatore.gruppi:
        raise HTTPException(status_code=403, detail="Utente non autorizzato")

    tappe = sorted(gruppo.percorso.tappe, key=lambda tappa: tappa.minuti_arrivo)
    if numero_tappa < 0 or numero_tappa >= len(tappe):
        raise HTTPException(status_code=404, detail="Tappa non trovata")

    tappa = tappe[numero_tappa]
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

    if gruppo not in current_user.orientatore.gruppi:
        raise HTTPException(status_code=403, detail="Utente non autorizzato")

    gruppo.numero_tappa = tappa
    gruppo.arrivato = arrivato
    db.commit()
    db.refresh(gruppo)

    return gruppo
