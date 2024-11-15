from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models import Utente
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
    return GruppoList
