import json
import logging

from fastapi import WebSocket, WebSocketDisconnect

from .dashboard.services import invia_admin_gruppi, invia_admin_orientati, invia_admin_aule
from .enums import UserRole
from .models import ConnectedUser
from .user.services import invia_users_gruppo, invia_user_gruppo
from ..services.orientatore.gruppo import get_gruppo_utente, set_next_tappa, set_previous_tappa

logger = logging.getLogger(__name__)


async def handle_request(self, websocket: WebSocket, user: ConnectedUser, websocket_manager):
    try:
        while True:
            data = await websocket.receive_text()
            data_json = json.loads(data)
            message_type = data_json.get("type")

            if message_type == "ping":
                await websocket.send_text(json.dumps({"type": "pong"}))

            if user.role == UserRole.ADMIN_DASHBOARD:
                await handle_admin_dashboard_request(self, websocket, user, websocket_manager, message_type)

            if user.role == UserRole.USER:
                await handle_user_request(self, websocket, user, websocket_manager, message_type)

    except WebSocketDisconnect:
        self.disconnect(str(user.user.id), user.role)
    except Exception as e:
        logger.exception(f"Errore nella gestione del messaggio: {str(e)}")


async def handle_admin_dashboard_request(self, websocket: WebSocket, user: ConnectedUser, websocket_manager,
                                         message_type: str):
    if message_type == "disconnect":
        self.disconnect(str(user.user.id), user.role)
        await websocket.close()
        logger.info(f"Disconnessione richiesta da {user.role}: {user.user.id}")
    elif message_type == "reload_groups":
        await invia_admin_gruppi(websocket)
    elif message_type == "reload_orientati":
        await invia_admin_orientati(websocket)
    elif message_type == "reload_aule":
        await invia_admin_aule(websocket)
    elif message_type == "reload_user_group":
        await invia_user_gruppo(user, websocket)
    else:
        logger.warning(f"Tipo messaggio sconosciuto: {message_type}")


async def handle_user_request(self, websocket: WebSocket, user: ConnectedUser, websocket_manager, message_type: str):
    if message_type == "next_step":  # TODO: deve inviare il gruppo aggiornato alla dashboard admin
        if user.role == UserRole.USER:
            set_next_tappa(gruppo_id=get_gruppo_utente(user.user.id))
            await invia_users_gruppo(get_gruppo_utente(user.user.id), websocket_manager)
        else:
            await websocket.send_text(json.dumps({
                "type": "error",
                "message": "Non autorizzato a passare alla tappa successiva"
            }))
    elif message_type == "previous_step":
        if user.role == UserRole.USER:
            set_previous_tappa(gruppo_id=get_gruppo_utente(user.user.id))
            await invia_users_gruppo(get_gruppo_utente(user.user.id), websocket_manager)
        else:
            await websocket.send_text(json.dumps({
                "type": "error",
                "message": "Non autorizzato a tornare alla tappa precedente"
            }))
    else:
        logger.warning(f"Tipo messaggio sconosciuto: {message_type}")
