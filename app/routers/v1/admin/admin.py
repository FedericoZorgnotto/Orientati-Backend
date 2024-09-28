from fastapi import APIRouter, Depends

from .users import users_router

admin_router = APIRouter()

admin_router.include_router(users_router)

@admin_router.get("/")
async def admin_root():
    """
    path di root dell'API admin

    restituisce un messaggio di benvenuto
    :return:
    """
    return {"message": "This is the admin root path"}
