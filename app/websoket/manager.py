import json
import logging
from typing import Dict

from fastapi import WebSocket, WebSocketDisconnect

from .auth import decode_token, get_user_from_payload, InvalidTokenError
from .dashboard.services import invia_admin_gruppi, invia_admin_orientati, invia_admin_aule
from .enums import UserRole
from .models import ConnectedUser
from .services import handle_request
from .user.services import invia_user_gruppo
from ..services.orientatore.gruppo import get_gruppo_utente

logger = logging.getLogger(__name__)

async def send_start_message(websocket: WebSocket, role: UserRole, user: ConnectedUser):
    if role == UserRole.ADMIN_DASHBOARD:
        await invia_admin_gruppi(websocket)
        await invia_admin_orientati(websocket)
        await invia_admin_aule(websocket)
    elif role == UserRole.USER:
        await invia_user_gruppo(user, websocket)


class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[UserRole, Dict[str, ConnectedUser]] = {
            role: {} for role in UserRole
        }

    async def handle_incoming_message(self, websocket: WebSocket, user: ConnectedUser):
        await handle_request(self, websocket, user, websocket_manager)

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        user = None
        role = None
        group_id = None
        try:
            message = json.loads(await websocket.receive_text())
            message_type = message.get("type", "")
            if message_type != "auth":
                await websocket.close(code=4000)
                return
            data = message.get("data")
            token = data.get("Authorization", "").split("Bearer ")[1]

            payload = None
            try:
                payload = decode_token(token)
            except InvalidTokenError:
                await websocket.send_text(json.dumps({"type": "error", "message": "Token non valido"}))
                await websocket.close(code=3000)
                return

            user = get_user_from_payload(payload)
            if not user:
                await websocket.close(code=4000)
                return
            role = UserRole.ADMIN_DASHBOARD if user.admin and data.get("dashboard") == "true" \
                else UserRole.ADMIN if user.admin else UserRole.USER
            if role == UserRole.USER:
                group_id = get_gruppo_utente(user.id)
            connected_user = ConnectedUser(user, websocket, role, group_id)
            self.active_connections[role][str(user.id)] = connected_user
            logger.info(f"Nuova connessione {role}: {user.id}")

            await websocket.send_text("connected " + str(role))
            await send_start_message(websocket, role, user)

            # Avvia la gestione dei messaggi
            await self.handle_incoming_message(websocket, connected_user)
        except WebSocketDisconnect:
            if user and role:
                self.disconnect(str(user.id), role)
        except Exception:
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
