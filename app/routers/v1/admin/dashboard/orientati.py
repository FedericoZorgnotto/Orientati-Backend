from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.middlewares.auth_middleware import admin_access
from app.models import Gruppo
from app.schemas.dashboard.orientato import OrientatoList, OrientatoBase

orientati_router = APIRouter()


@orientati_router.get("/", response_model=OrientatoList)
async def get_all_orientati(db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Legge tutti gli orientati dei gruppi che hanno data odierna, orientati per presenza
    """

    gruppi = db.query(Gruppo).filter(Gruppo.data == datetime.now().strftime("%d/%m/%Y")).all()
    orientati = []
    for gruppo in gruppi:
        for orientato in gruppo.orientati:
            presente = False
            for orientatoPresente in gruppo.presenti:
                if orientatoPresente.orientato_id == orientato.id:
                    presente = True
                    break

            orientati.append(OrientatoBase(
                nome=orientato.nome,
                cognome=orientato.cognome,
                scuolaDiProvenienza_nome=orientato.scuolaDiProvenienza.nome,
                presente= presente
            ))

    # ordinamento per presenza, prima quelli assenti
    orientati = sorted(orientati, key=lambda orientato: orientato.presente)

    return OrientatoList(orientati=orientati)

