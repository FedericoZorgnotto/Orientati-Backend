from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.middlewares.auth_middleware import admin_access
from app.models import Gruppo
from app.schemas.dashboard.gruppo import GruppoList, GruppoResponse
from app.schemas.tappa import TappaResponse

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


@gruppi_router.get("/tappe/{gruppo_id}", response_model=GruppoResponse)
async def get_tappe_gruppo(gruppo_id: int, db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Legge le tappe di un gruppo dal database
    """
    gruppo = db.query(Gruppo).filter(Gruppo.id == gruppo_id).first()
    if not gruppo:
        raise HTTPException(status_code=404, detail="Gruppo not found")
    return GruppoResponse.model_validate(gruppo)

@gruppi_router.get("/tappe/{gruppo_id}/{numero_tappa}", response_model=TappaResponse)
async def get_tappa_gruppo(gruppo_id: int, numero_tappa: int, db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Legge la tappa di un gruppo dal database
    """
    gruppo = db.query(Gruppo).filter(Gruppo.id == gruppo_id).first()
    if not gruppo:
        raise HTTPException(status_code=404, detail="Gruppo not found")
    if not gruppo.percorso.tappe[numero_tappa-1]:
        raise HTTPException(status_code=404, detail="Tappa not found")
    return TappaResponse(
        id=gruppo.percorso.tappe[numero_tappa-1].id,
        percorso_id=gruppo.percorso.tappe[numero_tappa-1].percorso.id,
        aula_id=gruppo.percorso.tappe[numero_tappa-1].aula.id,
        minuti_arrivo=gruppo.percorso.tappe[numero_tappa-1].minuti_arrivo,
        minuti_partenza=gruppo.percorso.tappe[numero_tappa-1].minuti_partenza
    )
