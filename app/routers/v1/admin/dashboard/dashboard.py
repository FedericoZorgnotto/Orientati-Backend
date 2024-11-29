from fastapi import APIRouter

from app.routers.v1.admin.dashboard.aule import aule_router
from app.routers.v1.admin.dashboard.gruppi import gruppi_router
from app.routers.v1.admin.dashboard.orientati import orientati_router

router = APIRouter()

router.include_router(gruppi_router, prefix="/gruppi")
router.include_router(orientati_router, prefix="/orientati")
router.include_router(aule_router, prefix="/aule")


@router.get("/")
async def admin_root():
    """
    path di root dell'API dashboard admin

    restituisce un messaggio di benvenuto
    :return:
    """
    return {"message": "This is the dashboard admin root path"}
