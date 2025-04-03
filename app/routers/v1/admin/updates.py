from fastapi import APIRouter, Depends

from app.middlewares.auth_middleware import admin_access
from app.schemas.admin.update import UpdateList, UpdateCreate, UpdateDelete, UpdateUpdate
from app.services.admin import updates

update_router = APIRouter()


@update_router.get("/", response_model=UpdateList)
async def get_all_updates(_=Depends(admin_access)):
    return updates.get_all_updates()


@update_router.post("/")
async def create_update(update: UpdateCreate, _=Depends(admin_access)):
    return {"message": "Update created successfully", "update": updates.create_update(update)}


@update_router.delete("/{update_id}", response_model=UpdateList)
async def delete_update(update: UpdateDelete, _=Depends(admin_access)):
    return {"message": "Update deleted successfully", "update": updates.delete_update(update)}


@update_router.put("/{update_id}", response_model=UpdateList)
async def update_update(update: UpdateUpdate, _=Depends(admin_access)):
    return {"message": "Update updated successfully", "update": updates.update_update(update)}


@update_router.get("/check_new_updates", response_model=bool)
async def check_new_updates(_=Depends(admin_access)):
    return updates.check_new_updates()


@update_router.get("/check_new_update/{update_id}", response_model=bool)
async def check_new_update(update_id: str, _=Depends(admin_access)):
    return updates.check_new_update(update_id)


@update_router.get("/update/{update_id}", response_model=bool)
async def get_update(update_id: str, _=Depends(admin_access)):
    return updates.get_update(update_id)


@update_router.get("/update_all")
async def update_all_updates(_=Depends(admin_access)):
    return updates.update_all_updates()
