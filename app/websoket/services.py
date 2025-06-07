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
            elif message_type == "disconnect":
                self.disconnect(str(user.user.id), user.role)
                await websocket.close()
                logger.info(f"Disconnessione richiesta da {user.role}: {user.user.id}")

            elif message_type == "reload_groups":
                if user.role == UserRole.ADMIN_DASHBOARD:
                    await invia_admin_gruppi(websocket)
                else:
                    await websocket.send_text(json.dumps({
                        "type": "error",
                        "message": "Non autorizzato a richiedere i gruppi"
                    }))
            elif message_type == "reload_orientati":
                if user.role == UserRole.ADMIN_DASHBOARD:
                    await invia_admin_orientati(websocket)
                else:
                    await websocket.send_text(json.dumps({
                        "type": "error",
                        "message": "Non autorizzato a richiedere gli orientati"
                    }))
            elif message_type == "reload_aule":
                if user.role == UserRole.ADMIN_DASHBOARD:
                    await invia_admin_aule(websocket)
                else:
                    await websocket.send_text(json.dumps({
                        "type": "error",
                        "message": "Non autorizzato a richiedere le aule"
                    }))

            elif message_type == "reload_user_group":
                if user.role == UserRole.USER:
                    await invia_user_gruppo(user, websocket)
                else:
                    await websocket.send_text(json.dumps({
                        "type": "error",
                        "message": "Non autorizzato a richiedere il gruppo utente"
                    }))
            elif message_type == "next_step":
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
    except WebSocketDisconnect:
        self.disconnect(str(user.user.id), user.role)
    except Exception as e:
        logger.exception(f"Errore nella gestione del messaggio: {str(e)}")
