from fastapi import APIRouter

from .statistiche import statistiche_router

router = APIRouter()

# router.include_router(indirizzi_router, prefix="/indirizzi")
# router.include_router(percorsiDiStudi_router, prefix="/percorsiDiStudi")
# router.include_router(utenti_router, prefix="/utenti")
# router.include_router(orientati_router, prefix="/orientati")
# router.include_router(scuoleDiProvenienza_router, prefix="/scuoleDiProvenienza")
# router.include_router(aule_router, prefix="/aule")
# router.include_router(tappe_router, prefix="/tappe")
# router.include_router(percorsi_router, prefix="/percorsi")
# router.include_router(gruppi_router, prefix="/gruppi")
# router.include_router(logsUtenti_router, prefix="/logsUtenti")
# router.include_router(dashboard_router, prefix="/dashboard")
router.include_router(statistiche_router, prefix="/statistiche")
