import json
import logging
from typing import Dict

from fastapi import WebSocket, WebSocketDisconnect

from .auth import decode_token, get_user_from_payload
from .enums import UserRole
from .models import ConnectedUser
from ..services.admin.dashboard.gruppi import get_all_gruppi

logger = logging.getLogger(__name__)

"""
Invia un messaggio di avvio al client dopo la connessione.
Questo metodo può essere esteso per inviare informazioni specifiche in base al ruolo dell'utente.
"""


async def send_start_message(websocket: WebSocket, role: UserRole, user: ConnectedUser):
    if role == UserRole.ADMIN_DASHBOARD:
        await websocket.send_text(json.dumps({"type": "gruppi", "data": str(get_all_gruppi())}))
        await websocket.send_text(str())


class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[UserRole, Dict[str, ConnectedUser]] = {
            role: {} for role in UserRole
        }

    async def handle_incoming_message(self, websocket: WebSocket, user: ConnectedUser):
        try:
            while True:
                data = await websocket.receive_text()
                data_json = json.loads(data)
                message_type = data_json.get("type")

                if message_type == "ping":
                    await websocket.send_text(json.dumps({"type": "pong"}))
                elif message_type == "update_dashboard" and user.role == UserRole.ADMIN_DASHBOARD:
                    gruppi = get_all_gruppi()
                    await websocket.send_text(str(gruppi))
                elif message_type == "disconnect":
                    self.disconnect(str(user.user.id), user.role)
                    await websocket.close()
                    logger.info(f"Disconnessione richiesta da {user.role}: {user.user.id}")

                elif message_type == "update_groups":
                    if user.role == UserRole.ADMIN_DASHBOARD:
                        await websocket.send_text(json.dumps({"type": "gruppi", "data": str(get_all_gruppi())}))
                    else:
                        logger.warning(f"Utente {user.user.id} non autorizzato a richiedere i gruppi")

                else:
                    logger.warning(f"Tipo messaggio sconosciuto: {message_type}")
        except WebSocketDisconnect:
            self.disconnect(str(user.user.id), user.role)
        except Exception as e:
            logger.exception(f"Errore nella gestione del messaggio: {str(e)}")

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
            if not user:
                await websocket.close(code=4000)
                return
            role = UserRole.ADMIN_DASHBOARD if user.admin and data_json.get("dashboard") == "true" \
                else UserRole.ADMIN if user.admin else UserRole.USER

            connected_user = ConnectedUser(user, websocket, role)
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
