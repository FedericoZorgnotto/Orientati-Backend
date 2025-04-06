import json
from datetime import datetime
from enum import Enum
from typing import Dict

from fastapi import WebSocket, HTTPException, WebSocketDisconnect
from jose import jwt, JWTError

from app.core.config import settings
from app.database import get_db
from app.models import Utente
from app.services.admin.dashboard.gruppi import get_all_gruppi


class UserRole(str, Enum):
    USER = "users"
    ADMIN = "admin"
    ADMIN_DASHBOARD = "adminDashboard"


def decode_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.algorithm])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Token non valido")


def get_user_from_payload(payload: dict):
    if "exp" in payload and datetime.fromtimestamp(payload["exp"]) < datetime.now():
        raise HTTPException(status_code=401, detail="Token scaduto")

    db = next(get_db())
    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Token non valido")

    user = db.query(Utente).filter(Utente.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Utente non trovato")
    return user

class ConnectedUser:
    def __init__(self, user: Utente, websocket: WebSocket, role: UserRole):
        self.user = user
        self.websocket = websocket
        self.role = role

class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[UserRole, Dict[str, WebSocket]] = {
            role: {} for role in UserRole
        }

    async def connect(self, websocket: WebSocket):
        """Accetta una nuova connessione WebSocket e verifica il token di autorizzazione"""
        await websocket.accept()

        try:
            data = await websocket.receive_text()
            data_json = json.loads(data)
            token = data_json.get("Authorization", "").split("Bearer ")[1] if "Authorization" in data_json else None
            if not token:
                await websocket.close(code=3000)
                return
            user = None
            try:
                user = get_user_from_payload(decode_token(token))
                if not user:
                    await websocket.close(code=3000)
                    return
            except Exception as e:
                print(e)
                await websocket.close(code=3000)
                return

            role = "admin" if user.admin else "users"
            if data_json.get("dashboard", False) and user.admin:
                role = "adminDashboard"
            self.active_connections[role][user.id] = ConnectedUser(user, websocket, role)
            print(f"Nuova connessione {role}: {user.id}")
            await websocket.send_text("connected")
        except WebSocketDisconnect:
            print("WebSocket chiuso")

    def disconnect(self, user_id: str, role: str):
        """Rimuove una connessione chiusa"""
        self.active_connections[role].pop(user_id, None)
        print(f"Connessione chiusa {role}: {user_id}")

    def disconnect_websocket(self, websocket: WebSocket):
        """Rimuove una connessione chiusa"""
        for role, connections in self.active_connections.items():
            for user_id, conn in connections.items():
                if conn == websocket:
                    self.active_connections[role].pop(user_id, None)
                    print(f"Connessione chiusa {role}: {user_id}")
                    return
        print("WebSocket chiuso")

    async def send_message(self, user_id: str, message: str, role: str):
        """Invia un messaggio a un utente specifico"""
        if user_id in self.active_connections[role]:
            await self.active_connections[role][user_id].send_text(message)

    async def broadcast(self, message: str, role: str):
        """Invia un messaggio a tutti gli utenti di un certo ruolo"""
        for user_id, websocket in list(self.active_connections[role].items()):
            try:
                await websocket.send_text(message)
            except WebSocketDisconnect:
                self.disconnect(user_id, role)
            except RuntimeError as e:
                self.disconnect(user_id, role)


websocket_manager = WebSocketManager()
