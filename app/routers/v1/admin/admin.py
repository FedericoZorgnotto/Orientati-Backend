from fastapi import APIRouter

from .aule import aule_router
from .dashboard.dashboard import router as dashboard_router
from .gruppi import gruppi_router
from .indirizzi import indirizzi_router
from .logsUtenti import logsUtenti_router
from .orientati import orientati_router
from .percorsi import percorsi_router
from .percorsiDiStudi import percorsiDiStudi_router
from .scuoleDiProvenienza import scuoleDiProvenienza_router
from .tappe import tappe_router
from .utenti import utenti_router

router = APIRouter()

router.include_router(indirizzi_router, prefix="/indirizzi")
router.include_router(percorsiDiStudi_router, prefix="/percorsiDiStudi")
router.include_router(utenti_router, prefix="/utenti")
router.include_router(orientati_router, prefix="/orientati")
router.include_router(scuoleDiProvenienza_router, prefix="/scuoleDiProvenienza")
router.include_router(aule_router, prefix="/aule")
router.include_router(tappe_router, prefix="/tappe")
router.include_router(percorsi_router, prefix="/percorsi")
router.include_router(gruppi_router, prefix="/gruppi")
router.include_router(logsUtenti_router, prefix="/logsUtenti")
router.include_router(dashboard_router, prefix="/dashboard")


@router.get("/")
async def admin_root():
    """
    path di root dell'API admin

    restituisce un messaggio di benvenuto
    :return:
    """
    return {"message": "This is the admin root path"}
