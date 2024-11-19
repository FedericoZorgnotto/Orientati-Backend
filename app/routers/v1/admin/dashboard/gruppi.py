from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.middlewares.auth_middleware import admin_access
from app.models import Gruppo
from app.schemas.dashboard.gruppo import GruppoList, GruppoResponse

gruppi_router = APIRouter()


@gruppi_router.get("/", response_model=GruppoList)
async def get_all_gruppi(db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Legge tutti i gruppi del giorno dal database
    """
    gruppi = db.query(Gruppo).filter(Gruppo.data == datetime.now().strftime("%d/%m/%Y")).all()
    listaGruppi = GruppoList(gruppi=[])
    listaGruppi.gruppi = [GruppoResponse.model_validate(gruppo) for gruppo in gruppi]
    for gruppo in listaGruppi.gruppi:
        gruppo.nomi_orientatori = []
        orientatori = db.query(Gruppo).filter(Gruppo.id == gruppo.id).all()
        for orientatore in orientatori:
            gruppo.nomi_orientatori.append(orientatore.nome)

    listaGruppi.gruppi = sorted(listaGruppi.gruppi, key=lambda gruppo: gruppo.orario_partenza)
    return listaGruppi