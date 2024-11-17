from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.middlewares.auth_middleware import admin_access
from app.models.logUtente import LogUtente
from app.schemas.logUtente import LogUtenteList, LogUtenteResponse

logsUtenti_router = APIRouter()


def convert_log_to_dict(log):
    log_dict = log.__dict__.copy()
    log_dict['orario'] = log.orario.isoformat()  # Convert datetime to string
    return log_dict


@logsUtenti_router.get("/", response_model=LogUtenteList)
async def get_all_logs(db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Legge tutti i log dal database
    """
    logs = db.query(LogUtente).order_by(LogUtente.orario.desc()).all()
    return LogUtenteList(logs=[LogUtenteResponse.model_validate(convert_log_to_dict(log)) for log in logs])


@logsUtenti_router.get("/{utente_id}", response_model=LogUtenteList)
async def get_utente_logs(utente_id: int, db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Legge tutti i log appartenenti ad un utente dal database
    """
    logs = db.query(LogUtente).order_by(LogUtente.orario.desc()).filter(LogUtente.utente_id == utente_id).all()
    return LogUtenteList(logs=[LogUtenteResponse.model_validate(convert_log_to_dict(log)) for log in logs])
