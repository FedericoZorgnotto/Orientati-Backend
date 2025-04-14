from fastapi import APIRouter, Depends

from app.middlewares.auth_middleware import genitoreRegistrato_access
from app.schemas.ragazzo import RagazzoList, RagazzoCreate, Ragazzo
from app.services.public.ragazzo import ragazzi_from_genitore, add_ragazzo

ragazzo_router = APIRouter()


@ragazzo_router.get("/", response_model=RagazzoList, summary="Leggi ragazzi da genitore")
async def get_ragazzi_from_genitore(genitore=Depends(genitoreRegistrato_access)):
    """
    Legge le informazioni dei ragazzi connessi al genitore
    """
    ragazzi = RagazzoList(ragazzi=[])
    ragazzi.ragazzi = ragazzi_from_genitore(genitore)
    return ragazzi


@ragazzo_router.post("/", response_model=Ragazzo, summary="Crea ragazzo")
async def create_ragazzo(ragazzo_data: RagazzoCreate, genitore=Depends(genitoreRegistrato_access)):
    """
    Crea un ragazzo
    """
    return add_ragazzo(ragazzo=ragazzo_data, genitore_id=genitore.id)
