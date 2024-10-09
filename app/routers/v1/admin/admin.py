from fastapi import APIRouter

from .users import users_router

router = APIRouter()

router.include_router(users_router)


@router.get("/")
async def admin_root():
    """
    path di root dell'API admin

    restituisce un messaggio di benvenuto
    :return:
    """
    return {"message": "This is the admin root path"}
