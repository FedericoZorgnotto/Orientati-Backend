from fastapi import WebSocket

from app.models.utente import Utente
from .enums import UserRole


class ConnectedUser:
    def __init__(self, user: Utente, websocket: WebSocket, role: UserRole, group_id: int = None,
                 percorso_id: int = None):
        self.user = user
        self.websocket = websocket
        self.role = role
        self.group_id = group_id  # ID del gruppo a cui l'utente è connesso, se applicabile
        self.percorso_id = percorso_id  # ID del percorso dell'utente, se applicabile
