from fastapi import APIRouter

from .date import date_router

router = APIRouter()

router.include_router(date_router, prefix="/date")
