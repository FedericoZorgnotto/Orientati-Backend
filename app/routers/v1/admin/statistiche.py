import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db, get_mongodb
from app.middlewares.auth_middleware import admin_access
from app.schemas.statistica import StatisticaList, StatisticaBase

statistiche_router = APIRouter()


@statistiche_router.get("/")
async def get_all_statistiche(db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Legge tutte le statistiche dal database
    """
    database = get_mongodb()
    stats_collection = database.get_collection(settings.MONGODB_STATS_COLLECTION)
    statistiche = StatisticaList(statistiche=[])
    async for document in stats_collection.find():
        statistiche.statistiche.append(StatisticaBase(
            data=datetime.datetime.fromisoformat(str(document["timestamp"])),
            cpu=float(document["cpu_percent"]),
            ram=float(document["ram_percent"])
        ))

    return statistiche
