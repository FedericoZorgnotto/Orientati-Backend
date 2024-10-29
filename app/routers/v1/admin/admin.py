from fastapi import APIRouter

from .orientatori import orientatori_router
from .utenti import utenti_router

router = APIRouter()

router.include_router(utenti_router, prefix="/utenti")
router.include_router(orientatori_router, prefix="/orientatori")


# router.include_router(groups_router, prefix="/guidance")


@router.get("/")
async def admin_root():
    """
    path di root dell'API admin

    restituisce un messaggio di benvenuto
    :return:
    """
    return {"message": "This is the admin root path"}
