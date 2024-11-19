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
    gruppi = db.query(Gruppo).filter(Gruppo.data == datetime.now().strftime("%Y-%m-%d")).all()
    return GruppoList(gruppi=[GruppoResponse.model_validate(gruppo) for gruppo in gruppi]) # TODO: aggiungere i nomi degli orientatori
