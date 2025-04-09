from fastapi import APIRouter

from .date import date_router
from .genitore import genitore_router

router = APIRouter()

router.include_router(date_router, prefix="/date")
router.include_router(genitore_router, prefix="/genitore")
