from fastapi import APIRouter

# from .percorsi import percorsi_router

router = APIRouter()

# router.include_router(percorsi_router, prefix="/percorsi")


@router.get("/")
async def orientatore_root():
    """
    path di root dell'API orientatore

    restituisce un messaggio di benvenuto
    :return:
    """
    return {"message": "This is the orientatore root path"}

