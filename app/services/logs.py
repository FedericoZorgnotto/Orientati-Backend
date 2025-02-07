import asyncio

from app.config import settings
from app.database import get_mongodb
from app.models.logUtente import CategoriaLogUtente as CategoriaLogUtenteEnum


async def log_user_action(categoria: CategoriaLogUtenteEnum, azione: str, utente_id: int = None, client_ip: str = None,
                          dati: {} = None):
    database = get_mongodb()
    while database is None:
        await asyncio.sleep(1)
        database = get_mongodb()
    logs_collection = database.get_collection(settings.MONGODB_LOGS_COLLECTION)

    if dati:
        dati = {k: str(v) for k, v in dati.items()}

    log_entry = {
        "utente_id": utente_id,
        "categoria": categoria.value,
        "azione": azione,
        "client_ip": client_ip,
        "dati": dati
    }

    logs_collection.insert_one(log_entry)
