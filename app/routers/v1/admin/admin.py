from fastapi import APIRouter

from .guidance.groups import groups_router
from .guidance.rooms import rooms_router
from .guidance.routes import routes_router
from .guidance.stages import stages_router
from .specialisations import specialisations_router
from .users import users_router

router = APIRouter()

router.include_router(users_router)
router.include_router(specialisations_router)
router.include_router(groups_router, prefix="/guidance")
router.include_router(routes_router, prefix="/guidance")
router.include_router(stages_router, prefix="/guidance")
router.include_router(rooms_router, prefix="/guidance")


@router.get("/")
async def admin_root():
    """
    path di root dell'API admin

    restituisce un messaggio di benvenuto
    :return:
    """
    return {"message": "This is the admin root path"}
