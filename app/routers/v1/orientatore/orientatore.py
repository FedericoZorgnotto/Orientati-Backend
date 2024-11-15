from fastapi import APIRouter

from .gruppi import gruppo_router

router = APIRouter()

router.include_router(gruppo_router, prefix="/gruppo")


@router.get("/")
async def orientatore_root():
    """
    path di root dell'API orientatore

    restituisce un messaggio di benvenuto
    :return:
    """
    return {"message": "This is the orientatore root path"}
