import json

from fastapi import APIRouter, Depends, HTTPException, status

from app.config import settings
from app.database import get_mongodb
from app.middlewares.auth_middleware import admin_access
from app.schemas.logUtente import LogUtenteList, LogUtenteResponse

logsUtenti_router = APIRouter()


@logsUtenti_router.get("/", response_model=LogUtenteList)
async def get_all_logs(_=Depends(admin_access)):
    """
    Legge tutti i log dal database
    """
    try:
        database = get_mongodb()
        logs_collection = database.get_collection(settings.MONGODB_LOGS_COLLECTION)
        logs = await logs_collection.find().sort("timestamp", -1).to_list()
        return LogUtenteList(logs=[LogUtenteResponse(
            id=str(log['_id']),
            timestamp=log['timestamp'].isoformat(),
            utente_id=log['utente_id'],
            categoria=log['categoria'],
            azione=log['azione'],
            client_ip=log['client_ip'],
            dati=json.dumps(log['dati'])
        ) for log in logs])

    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@logsUtenti_router.get("/{utente_id}", response_model=LogUtenteList)
async def get_utente_logs(utente_id: int, _=Depends(admin_access)):
    """
    Legge tutti i log appartenenti ad un utente dal database
    """
    try:
        database = get_mongodb()
        logs_collection = database.get_collection(settings.MONGODB_LOGS_COLLECTION)
        logs = logs_collection.find({"utente_id": utente_id}).sort("timestamp", -1)
        return LogUtenteList(logs=[LogUtenteResponse(
            id=str(log['_id']),
            timestamp=log['timestamp'].isoformat(),
            utente_id=log['utente_id'],
            categoria=log['categoria'],
            azione=log['azione'],
            client_ip=log['client_ip'],
            dati=json.dumps(log['dati'])
        ) async for log in logs])
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
