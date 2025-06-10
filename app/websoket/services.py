import json
import logging

from fastapi import WebSocket, WebSocketDisconnect

from .dashboard.services import invia_admin_gruppi, invia_admin_orientati, invia_admin_aule, genera_codice_gruppo, \
    invia_utenti_gruppo, rimuovi_utente_gruppo, modifica_gruppo_iscrizione, modifica_ragazzo_presente, \
    modifica_ragazzo_assente, modifica_ragazzo_non_arrivato, modifica_fascia_oraria_orario_partenza, \
    modifica_gruppo_nome, modifica_gruppo_tappa, crea_ragazzo_gruppo, get_scuole_di_provenienza, get_genitori, \
    crea_ragazzo_iscrizione, get_ragazzi, collega_ragazzo_iscrizione
from .enums import UserRole
from .models import ConnectedUser
from .user.services import invia_users_gruppo
from ..services.orientatore.gruppo import get_gruppo_utente, set_next_tappa, set_previous_tappa

logger = logging.getLogger(__name__)


async def handle_request(self, websocket: WebSocket, user: ConnectedUser, websocket_manager):
    try:
        while True:
            message = json.loads(await websocket.receive_text())
            message_type = message.get("type")
            message_data = message.get("data")

            if message_type == "ping":
                await websocket.send_text(json.dumps({"type": "pong"}))

            if user.role == UserRole.ADMIN_DASHBOARD:
                await handle_admin_dashboard_request(self, websocket, user, websocket_manager, message_type,
                                                     message_data)

            if user.role == UserRole.USER:
                await handle_user_request(self, websocket, user, websocket_manager, message_type, message_data)

    except WebSocketDisconnect:
        self.disconnect(str(user.user.id), user.role)
    except Exception as e:
        logger.exception(f"Errore nella gestione del messaggio: {str(e)}")


async def handle_admin_dashboard_request(self, websocket: WebSocket, user: ConnectedUser, websocket_manager,
                                         message_type: str, message_data: dict):
    if message_type == "disconnect":
        self.disconnect(str(user.user.id), user.role)
        await websocket.close()
        logger.info(f"Disconnessione richiesta da {user.role}: {user.user.id}")

    elif message_type == "reload_groups":
        await invia_admin_gruppi(websocket, user.percorso_id)
    elif message_type == "reload_orientati":
        await invia_admin_orientati(websocket, user.percorso_id)
    elif message_type == "reload_aule":
        await invia_admin_aule(websocket, user.percorso_id)

    elif message_type == "generate_group_code":
        await genera_codice_gruppo(websocket, message_data.get("group_id"))
    elif message_type == "get_group_users":
        await invia_utenti_gruppo(websocket, message_data.get("group_id"))
    elif message_type == "remove_user_from_group":
        await rimuovi_utente_gruppo(websocket, message_data.get("user_id"), message_data.get("group_id"))

    elif message_type == "change_iscrizione_group":
        await modifica_gruppo_iscrizione(websocket, message_data.get("group_id"), message_data.get("iscrizione_id"))

    elif message_type == "change_ragazzo_presente":
        await modifica_ragazzo_presente(websocket, message_data.get("ragazzo_id"), message_data.get("group_id"))
    elif message_type == "change_ragazzo_assente":
        await modifica_ragazzo_assente(websocket, message_data.get("ragazzo_id"), message_data.get("group_id"))
    elif message_type == "change_ragazzo_non_arrivato":
        await modifica_ragazzo_non_arrivato(websocket, message_data.get("ragazzo_id"), message_data.get("group_id"))

    elif message_type == "change_fascia_oraria_orario_partenza":
        await modifica_fascia_oraria_orario_partenza(websocket, message_data.get("fascia_oraria_id"),
                                                     message_data.get("orario_partenza"))
    elif message_type == "change_group_name":
        await modifica_gruppo_nome(websocket, message_data.get("group_id"), message_data.get("new_name"))
    elif message_type == "change_group_tappa":
        await modifica_gruppo_tappa(websocket, message_data.get("group_id"), message_data.get("numero_tappa"),
                                    message_data.get("arrivato"))


    elif message_type == "create_ragazzo_group":
        await crea_ragazzo_gruppo(websocket, message_data.get("group_id"), message_data.get("name"),
                                  message_data.get("surname"), message_data.get("scuolaDiProvenienza_id"),
                                  message_data.get("genitore_id"))
    elif message_type == "create_ragazzo_iscrizione":
        await crea_ragazzo_iscrizione(websocket, message_data.get("iscrizione_id"), message_data.get("name"),
                                      message_data.get("surname"), message_data.get("scuolaDiProvenienza_id"))

    elif message_type == "get_scuole_di_provenienza":
        await get_scuole_di_provenienza(websocket)
    elif message_type == "get_genitori":
        await get_genitori(websocket)
    elif message_type == "get_ragazzi":
        await get_ragazzi(websocket)

    elif message_type == "link_ragazzo_iscrizione":
        await collega_ragazzo_iscrizione(websocket, message_data.get("ragazzo_id"), message_data.get("iscrizione_id"))

    else:
        logger.warning(f"Tipo messaggio sconosciuto: {message_type}")


async def handle_user_request(self, websocket: WebSocket, user: ConnectedUser, websocket_manager, message_type: str,
                              message_data: dict):
    if message_type == "next_step":  # TODO: deve inviare il gruppo aggiornato alla dashboard admin
        set_next_tappa(gruppo_id=get_gruppo_utente(user.user.id))
        await invia_users_gruppo(get_gruppo_utente(user.user.id), websocket_manager)

    elif message_type == "previous_step":
        set_previous_tappa(gruppo_id=get_gruppo_utente(user.user.id))
        await invia_users_gruppo(get_gruppo_utente(user.user.id), websocket_manager)


    # TODO: aggiungere che un0utente possa collegarsi ad un gruppo tramite codice

    else:
        logger.warning(f"Tipo messaggio sconosciuto: {message_type}")
