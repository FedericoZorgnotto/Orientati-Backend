from fastapi import APIRouter, Depends

from app.middlewares.auth_middleware import genitoreRegistrato_access
from app.schemas.ragazzo import RagazzoList, RagazzoCreate, Ragazzo
from app.services.public.ragazzo import ragazzi_from_genitore, add_ragazzo, ragazzo_from_ragazzo_id, \
    delete_ragazzo_from_ragazzo_id, edit_ragazzo

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


@ragazzo_router.get("/{ragazzo_id}", response_model=Ragazzo, summary="Leggi ragazzo")
async def get_ragazzo(ragazzo_id: int, genitore=Depends(genitoreRegistrato_access)):
    """
    Legge le informazioni di un ragazzo
    """
    ragazzo = ragazzo_from_ragazzo_id(ragazzo_id)
    if not ragazzo:
        return None
    if ragazzo.genitore_id != genitore.id:
        return None
    return ragazzo


@ragazzo_router.delete("/{ragazzo_id}", response_model=Ragazzo, summary="Elimina ragazzo")
async def delete_ragazzo(ragazzo_id: int, genitore=Depends(genitoreRegistrato_access)):
    """
    Elimina un ragazzo
    """
    # controllo che il ragazzo appartenga al genitore
    ragazzo = ragazzo_from_ragazzo_id(ragazzo_id)
    if not ragazzo:
        return None
    if ragazzo.genitore_id != genitore.id:
        return None

    return delete_ragazzo_from_ragazzo_id(ragazzo_id)


@ragazzo_router.put("/{ragazzo_id}", response_model=Ragazzo, summary="Modifica ragazzo")
async def update_ragazzo(ragazzo_id: int, ragazzo_data: RagazzoCreate, genitore=Depends(genitoreRegistrato_access)):
    """
    Modifica i dati di un ragazzo esistente
    """
    # controllo che il ragazzo appartenga al genitore
    ragazzo = ragazzo_from_ragazzo_id(ragazzo_id)
    if not ragazzo:
        return None
    if ragazzo.genitore_id != genitore.id:
        return None

    return edit_ragazzo(ragazzo=ragazzo, ragazzo_data=ragazzo_data)
