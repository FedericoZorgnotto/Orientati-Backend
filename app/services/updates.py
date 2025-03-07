import os
import subprocess

import requests


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
