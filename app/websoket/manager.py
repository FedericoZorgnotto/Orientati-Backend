import json
import logging
from typing import Dict

from fastapi import WebSocket, WebSocketDisconnect

from .auth import decode_token, get_user_from_payload
from .models import ConnectedUser
from .enums import UserRole
from app.services.admin.dashboard.gruppi import get_all_gruppi

logger = logging.getLogger(__name__)


class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[UserRole, Dict[str, ConnectedUser]] = {
            role: {} for role in UserRole
        }

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        user = None
        role = None

        try:
            data = await websocket.receive_text()
            data_json = json.loads(data)
            token = data_json.get("Authorization", "").split("Bearer ")[1]

            payload = decode_token(token)
            user = get_user_from_payload(payload)

            role = UserRole.ADMIN_DASHBOARD if user.admin and data_json.get("dashboard") \
                else UserRole.ADMIN if user.admin else UserRole.USER

            self.active_connections[role][user.id] = ConnectedUser(user, websocket, role)
            logger.info(f"Nuova connessione {role}: {user.id}")

            await websocket.send_text("connected")
            await websocket.send_text(str(get_all_gruppi()))

        except WebSocketDisconnect:
            if user and role:
                self.disconnect(user.id, role)
        except Exception as e:
            logger.exception("Errore nella connessione WebSocket")
            await websocket.close(code=3000)

    def disconnect(self, user_id: str, role: UserRole):
        self.active_connections[role].pop(user_id, None)
        logger.info(f"Connessione chiusa {role}: {user_id}")

    def disconnect_websocket(self, websocket: WebSocket):
        for role, conns in self.active_connections.items():
            for user_id, conn in conns.items():
                if conn.websocket == websocket:
                    self.disconnect(user_id, role)
                    return

    async def send_message(self, user_id: str, message: str, role: UserRole):
        conn = self.active_connections[role].get(user_id)
        if conn:
            await conn.websocket.send_text(message)

    async def broadcast(self, message: str, role: UserRole):
        for user_id, conn in list(self.active_connections[role].items()):
            try:
                await conn.websocket.send_text(message)
            except WebSocketDisconnect:
                self.disconnect(user_id, role)
            except RuntimeError:
                self.disconnect(user_id, role)

websocket_manager = WebSocketManager()
