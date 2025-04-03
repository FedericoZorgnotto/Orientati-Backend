import os

from fastapi import APIRouter, Depends, HTTPException

from app.core.config import settings
from app.database import get_mongodb
from app.middlewares.auth_middleware import admin_access
from app.schemas.admin.update import UpdateList, UpdateCreate, UpdateDelete, UpdateUpdate
from app.services.updates import repo_exists, clone_repo, get_local_version, get_latest_version, update_repo

update_router = APIRouter()


@update_router.get("/", response_model=UpdateList)
async def get_all_updates(_=Depends(admin_access)):
    """
    Legge tutti gli update impostati dal database
    """
    database = get_mongodb()
    updates_collection = database.get_collection(settings.MONGODB_UPDATES_COLLECTION)
    updates = UpdateList(updates=[])
    async for document in updates_collection.find():
        document["_id"] = str(document["_id"])
        local_version = get_local_version(document["directory"])
        new_version = get_latest_version(document["repo_owner"], document["repo_name"])
        document["aggiornato"] = local_version == new_version
        updates.updates.append(document)

    return updates


@update_router.post("/")
async def create_update(update: UpdateCreate, _=Depends(admin_access)):
    """
    Crea un nuovo update
    """
    if not update.nome and not update.repo_owner or not update.repo_name or not update.directory:
        raise HTTPException(status_code=400, detail="Missing required fields")

    if not repo_exists(update.repo_owner, update.repo_name):
        raise HTTPException(status_code=404, detail="Repository not found")
    if os.path.exists(os.path.normpath(update.directory)):
        raise HTTPException(status_code=400, detail="Repository already exists")
    clone_repo(update.repo_owner, update.repo_name, update.directory)
    database = get_mongodb()
    updates_collection = database.get_collection(settings.MONGODB_UPDATES_COLLECTION)
    updates_collection.insert_one(update.model_dump())
    return {"message": "Update created successfully", "update": update}


@update_router.delete("/{update_id}", response_model=UpdateList)
async def delete_update(update: UpdateDelete, _=Depends(admin_access)):
    """
    Elimina un update
    """
    database = get_mongodb()
    updates_collection = database.get_collection("updates")
    await updates_collection.delete_one({"_id": update.id})
    return await get_all_updates()


@update_router.put("/{update_id}", response_model=UpdateList)
async def update_update(update: UpdateUpdate, _=Depends(admin_access)):
    """
    Modifica un update
    """
    database = get_mongodb()
    updates_collection = database.get_collection("updates")
    await updates_collection.update_one({"_id": update["_id"]}, {"$set": update})
    return await get_all_updates()


@update_router.get("/check_new_updates", response_model=bool)
async def check_new_updates(_=Depends(admin_access)):
    """
    Controlla se ci sono nuovi aggiornamenti tra tutti gli update
    """
    database = get_mongodb()
    updates_collection = database.get_collection(settings.MONGODB_UPDATES_COLLECTION)
    async for update in updates_collection.find():
        local_version = get_local_version(update["directory"])
        new_version = get_latest_version(update["repo_owner"], update["repo_name"])
        if local_version != new_version:
            return True
    return False


@update_router.get("/check_new_update/{update_id}", response_model=bool)
async def check_new_update(update_id: str, _=Depends(admin_access)):
    """
    Controlla se c'è un nuovo aggiornamento per un singolo update
    """
    database = get_mongodb()
    updates_collection = database.get_collection(settings.MONGODB_UPDATES_COLLECTION)
    update = await updates_collection.find_one({"_id": update_id})
    local_version = get_local_version(update["directory"])
    new_version = get_latest_version(update["repo_owner"], update["repo_name"])
    return local_version != new_version


@update_router.get("/update/{update_id}", response_model=bool)
async def get_update(update_id: str, _=Depends(admin_access)):
    """
    Aggiorna un update
    """
    database = get_mongodb()
    updates_collection = database.get_collection(settings.MONGODB_UPDATES_COLLECTION)
    update = await updates_collection.find_one({"_id": update_id})
    update_repo(update["repo_owner"], update["repo_name"], update["directory"])
    return True


@update_router.get("/update_all")
async def update_all_updates(_=Depends(admin_access)):
    """
    Aggiorna tutti gli update
    """
    database = get_mongodb()
    updates_collection = database.get_collection(settings.MONGODB_UPDATES_COLLECTION)
    async for update in updates_collection.find():
        update_repo(update["repo_owner"], update["repo_name"], update["directory"])
    return {"message": "Updates updated successfully"}
