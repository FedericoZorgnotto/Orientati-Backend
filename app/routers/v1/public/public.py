from fastapi import APIRouter

from .date import date_router
from .genitore import genitore_router
from .iscrizione import iscrizione_router
from .ragazzo import ragazzo_router
from .scuolaDiProvenienza import scuola_router

router = APIRouter()

router.include_router(date_router, prefix="/date", tags=["Date"])
router.include_router(genitore_router, prefix="/genitore", tags=["Genitore"])
router.include_router(ragazzo_router, prefix="/ragazzo", tags=["Ragazzo"])
router.include_router(scuola_router, prefix="/scuola", tags=["Scuola"])
router.include_router(iscrizione_router, prefix="/iscrizione", tags=["Iscrizione"])
