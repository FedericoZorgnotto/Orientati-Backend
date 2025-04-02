from typing import Dict
from fastapi import WebSocket

class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[str, Dict[str, WebSocket]] = {
            "users": {},  # Connessioni utenti normali
            "admin": {}   # Connessioni admin
        }

    async def connect(self, websocket: WebSocket, user_id: str, role: str):
        """Accetta una nuova connessione WebSocket in base al ruolo"""
        await websocket.accept()
        self.active_connections[role][user_id] = websocket
        print(f"📡 Nuova connessione {role}: {user_id}")

    def disconnect(self, user_id: str, role: str):
        """Rimuove una connessione chiusa"""
        self.active_connections[role].pop(user_id, None)
        print(f"❌ Connessione chiusa {role}: {user_id}")

    async def send_message(self, user_id: str, message: str, role: str):
        """Invia un messaggio a un utente specifico"""
        if user_id in self.active_connections[role]:
            await self.active_connections[role][user_id].send_text(message)

    async def broadcast(self, message: str, role: str):
        """Invia un messaggio a tutti gli utenti di un certo ruolo"""
        for websocket in self.active_connections[role].values():
            await websocket.send_text(message)

websocket_manager = WebSocketManager()
