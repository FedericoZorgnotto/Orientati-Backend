from charset_normalizer import from_path
from fastapi import APIRouter

from .users import users_router
from .specialisations import specialisations_router
from .guidance.groups import groups_router
from .guidance.routes import routes_router
from .guidance.stages import stages_router
from .guidance.rooms import rooms_router

router = APIRouter()

router.include_router(users_router)
router.include_router(specialisations_router)
router.include_router(groups_router)
router.include_router(routes_router)



@router.get("/")
async def admin_root():
    """
    path di root dell'API admin

    restituisce un messaggio di benvenuto
    :return:
    """
    return {"message": "This is the admin root path"}
