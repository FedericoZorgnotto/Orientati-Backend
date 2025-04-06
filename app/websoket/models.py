from fastapi import WebSocket
from app.models.utente import Utente
from .enums import UserRole

class ConnectedUser:
    def __init__(self, user: Utente, websocket: WebSocket, role: UserRole):
        self.user = user
        self.websocket = websocket
        self.role = role
