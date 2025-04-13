from fastapi import APIRouter

from .date import date_router
from .genitore import genitore_router
from .ragazzo import ragazzo_router

router = APIRouter()

router.include_router(date_router, prefix="/date", tags=["Date"])
router.include_router(genitore_router, prefix="/genitore", tags=["Genitore"])

router.include_router(ragazzo_router, prefix="/ragazzo", tags=["Ragazzo"])
