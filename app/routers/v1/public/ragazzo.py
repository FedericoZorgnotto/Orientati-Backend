from fastapi import APIRouter, Depends

from app.middlewares.auth_middleware import genitoreRegistrato_access
from app.schemas.ragazzo import RagazzoList
from app.services.public.ragazzo import ragazzi_from_genitore

ragazzo_router = APIRouter()


@ragazzo_router.get("/", response_model=RagazzoList, summary="Leggi informazioni genitore")
async def get_ragazzi_from_genitore(genitore=Depends(genitoreRegistrato_access)):
    """
    Legge le informazioni dei ragazzi connessi al genitore
    """
    gaga = RagazzoList(ragazzi=[])
    gaga.ragazzi = ragazzi_from_genitore(genitore)
    return gaga
