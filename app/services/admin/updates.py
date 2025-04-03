import os
import subprocess

import requests
from fastapi import HTTPException

from app.core.config import settings
from app.database import get_mongodb
from app.schemas.admin.update import UpdateList, UpdateCreate, UpdateDelete, UpdateUpdate
from app.websocket_manager import websocket_manager


async def get_all_updates():
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


async def create_update(update: UpdateCreate):
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
    return update


async def delete_update(update: UpdateDelete):
    """
    Elimina un update
    """
    database = get_mongodb()
    updates_collection = database.get_collection("updates")
    await updates_collection.delete_one({"_id": update.id})
    return await get_all_updates()


async def update_update(update: UpdateUpdate):
    """
    Modifica un update
    """
    database = get_mongodb()
    updates_collection = database.get_collection("updates")
    await updates_collection.update_one({"_id": update["_id"]}, {"$set": update})
    return await get_all_updates()


async def check_new_updates():
    """
    Controlla se ci sono nuovi aggiornamenti tra tutti gli update
    """
    database = get_mongodb()
    updates_collection = database.get_collection(settings.MONGODB_UPDATES_COLLECTION)
    async for update in updates_collection.find():
        local_version = get_local_version(update["directory"])
        new_version = get_latest_version(update["repo_owner"], update["repo_name"])
        if local_version != new_version:
            websocket_manager.broadcast("update_available", {"admin"})
            return True
    return False


async def check_new_update(update_id: str):
    """
    Controlla se c'è un nuovo aggiornamento per un singolo update
    """
    database = get_mongodb()
    updates_collection = database.get_collection(settings.MONGODB_UPDATES_COLLECTION)
    update = await updates_collection.find_one({"_id": update_id})
    local_version = get_local_version(update["directory"])
    new_version = get_latest_version(update["repo_owner"], update["repo_name"])
    if local_version != new_version:
        websocket_manager.broadcast("update_available", {"admin"})
    return local_version != new_version


async def get_update(update_id: str):
    """
    Aggiorna un update
    """
    database = get_mongodb()
    updates_collection = database.get_collection(settings.MONGODB_UPDATES_COLLECTION)
    update = await updates_collection.find_one({"_id": update_id})
    update_repo(update["repo_owner"], update["repo_name"], update["directory"])
    return True


async def update_all_updates():
    """
    Aggiorna tutti gli update
    """
    database = get_mongodb()
    updates_collection = database.get_collection(settings.MONGODB_UPDATES_COLLECTION)
    async for update in updates_collection.find():
        update_repo(update["repo_owner"], update["repo_name"], update["directory"])
    return True


# region gestione repo


def repo_exists(owner: str, repo: str) -> bool:
    """Verifica se una repository esiste su GitHub."""
    url = f"https://api.github.com/repos/{owner}/{repo}"
    response = requests.get(url)
    return response.status_code == 200


def get_latest_version(owner: str, repo: str, include_prerelease: bool = True) -> str:
    """Ottiene l'ultima versione di una repository GitHub."""
    url = f"https://api.github.com/repos/{owner}/{repo}/releases"
    response = requests.get(url)

    if response.status_code != 200:
        raise ValueError("Impossibile ottenere le release.")

    releases = response.json()

    if not releases:
        return "Nessuna release trovata"

    if not include_prerelease:
        releases = [r for r in releases if not r["prerelease"]]

    return releases[0]["tag_name"] if releases else "Nessuna release stabile trovata"


def get_local_version(repo_path: str) -> str | None:
    """Ottiene la versione attuale della repository locale."""
    try:
        version = subprocess.check_output(["git", "describe", "--tags"], cwd=repo_path).decode().strip()
        return version
    except subprocess.CalledProcessError:
        return None


def clone_repo(owner: str, repo: str, directory: str, include_prerelease: bool = True):
    """Clona la repository GitHub all'ultima versione pubblicata."""
    latest_version = get_latest_version(owner, repo, include_prerelease)

    if not latest_version:
        raise ValueError("Nessuna release valida trovata.")

    repo_url = f"https://github.com/{owner}/{repo}.git"
    directory = directory or f"{repo}-{latest_version}"

    if os.path.exists(directory):
        raise FileExistsError(f"La directory '{directory}' esiste già.")

    # Clona la repository
    subprocess.run(["git", "clone", repo_url, directory], check=True)

    # Spostarsi all'ultima versione (tag)
    subprocess.run(["git", "checkout", f"tags/{latest_version}"], cwd=directory, check=True)


def update_repo(owner: str, repo: str, repo_path: str, include_prerelease: bool = True):
    """Aggiorna la repository locale all'ultima versione disponibile."""
    if not os.path.exists(repo_path):
        raise FileNotFoundError(f"La cartella '{repo_path}' non esiste.")

    latest_version = get_latest_version(owner, repo, include_prerelease)
    if not latest_version:
        raise ValueError("Nessuna release disponibile.")

    local_version = get_local_version(repo_path)

    if local_version == latest_version:
        return

    subprocess.run(["git", "fetch", "--tags"], cwd=repo_path, check=True)
    subprocess.run(["git", "checkout", f"tags/{latest_version}"], cwd=repo_path, check=True)

# endregion
