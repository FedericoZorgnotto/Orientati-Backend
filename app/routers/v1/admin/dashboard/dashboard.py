from fastapi import APIRouter

from app.routers.v1.admin.dashboard.gruppi import gruppi_router

router = APIRouter()

router.include_router(gruppi_router, prefix="/gruppi")


@router.get("/")
async def admin_root():
    """
    path di root dell'API dashboard admin

    restituisce un messaggio di benvenuto
    :return:
    """
    return {"message": "This is the dashboard admin root path"}
