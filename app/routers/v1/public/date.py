from fastapi import APIRouter

from app.schemas.date import DataList
from app.services.public.date import get_all_date, get_available_date

date_router = APIRouter()


@date_router.get("/", response_model=DataList, summary="Lista date")
async def get_all():
    """
    Legge tutte le date con le fasce orarie
    """
    date = get_all_date()
    return {"date": date}


@date_router.get("/available", response_model=DataList, summary="Lista date disponibili")
async def get_available():
    """
    Legge tutte le date ancora disponibili con le relative fasce orarie
    """
    date = get_available_date()
    return {"date": date}
