from fastapi import APIRouter

from app.schemas.date import DataList
from app.services.public.date import get_all_date

date_router = APIRouter()


@date_router.get("/", response_model=DataList, summary="Lista date disponibili")
async def get_all():
    """
    Legge tutte le date disponibili con le fasce orarie
    """
    date = get_all_date()
    return {"date": date}
