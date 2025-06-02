import json
import logging
from typing import Dict

from fastapi import WebSocket, WebSocketDisconnect

from .auth import decode_token, get_user_from_payload
from .enums import UserRole
from .models import ConnectedUser
from ..services.admin.dashboard.aule import get_all_aule
from ..services.admin.dashboard.gruppi import get_all_gruppi
from ..services.admin.dashboard.orientati import get_all_orientati
from ..services.orientatore.gruppo import get_gruppo_utente

logger = logging.getLogger(__name__)

"""
Invia un messaggio di avvio al client dopo la connessione.
Questo metodo può essere esteso per inviare informazioni specifiche in base al ruolo dell'utente.
"""


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
                        await invia_admin_gruppi(websocket)
                    else:
                        logger.warning(f"Utente {user.user.id} non autorizzato a richiedere i gruppi")
                elif message_type == "update_orientati":
                    if user.role == UserRole.ADMIN_DASHBOARD:
                        await invia_admin_orientati(websocket)
                    else:
                        logger.warning(f"Utente {user.user.id} non autorizzato a richiedere gli orientati")
                elif message_type == "update_aule":
                    if user.role == UserRole.ADMIN_DASHBOARD:
                        await invia_admin_aule(websocket)
                    else:
                        logger.warning(f"Utente {user.user.id} non autorizzato a richiedere le aule")

                elif message_type == "update_user_group":
                    if user.role == UserRole.USER:
                        await invia_user_gruppo(user, websocket)
                    else:
                        logger.warning(f"Utente {user.user.id} non autorizzato a richiedere il proprio gruppo utente")
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

            payload = None
            try:
                payload = decode_token(token)
            except Exception as e:
                logger.error(f"Token non valido: {e}")
                await websocket.send_text(json.dumps({"type": "error", "message": "Token non valido"}))
                await websocket.close(code=3000)
                return

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


async def invia_user_gruppo(user: ConnectedUser, websocket: WebSocket):
    gruppo_utente = None
    try:
        gruppo_utente = get_gruppo_utente(user.id)
    except Exception as e:
        await websocket.send_text(json.dumps({
            "type": "error",
            "message": str(e)
        }))
    if not gruppo_utente:
        await websocket.send_text(json.dumps({
            "type": "error",
            "message": "Utente non connesso a nessun gruppo"
        }))
        await websocket.close(code=4000)
        return

    await websocket.send_text(json.dumps({
        "type": "gruppo",
        "gruppo": {
            "nome": gruppo_utente.nome,
            "orario_partenza": gruppo_utente.orario_partenza,
            "percorso_id": gruppo_utente.percorso_id,
            "numero_tappa": gruppo_utente.numero_tappa,
            "arrivato": gruppo_utente.arrivato,
            "percorso_finito": gruppo_utente.percorso_finito,
            "id": gruppo_utente.id,
            "orientati_presenti": gruppo_utente.orientati_presenti,
            "orientati_assenti": gruppo_utente.orientati_assenti,
            "orientati_totali": gruppo_utente.orientati_totali
        }
    }))

async def invia_admin_aule(websocket: WebSocket):
    await websocket.send_text(json.dumps({
        "type": "aule",
        "aule": [{
            "id": a.id,
            "nome": a.nome,
            "posizione": a.posizione,
            "materia": a.materia,
            "dettagli": a.dettagli,
            "occupata": a.occupata,
            "gruppo_id": a.gruppo_id,
            "gruppo_nome": a.gruppo_nome,
            "gruppo_orario_partenza": a.gruppo_orario_partenza,
            "minuti_arrivo": a.minuti_arrivo,
            "minuti_partenza": a.minuti_partenza
        } for a in get_all_aule().aule]
    }))

async def invia_admin_orientati(websocket: WebSocket):
    await websocket.send_text(json.dumps({
        "type": "orientati",
        "orientati": [{
            "id": o.id,
            "nome": o.nome,
            "cognome": o.cognome,
            "scuolaDiProvenienza_id": o.scuolaDiProvenienza_id,
            "scuolaDiProvenienza_nome": o.scuolaDiProvenienza_nome,
            "gruppo_id": o.gruppo_id,
            "gruppo_nome": o.gruppo_nome,
            "gruppo_orario_partenza": o.gruppo_orario_partenza,
            "presente": o.presente,
            "assente": o.assente
        } for o in get_all_orientati().orientati]
    }))

async def invia_admin_gruppi(websocket: WebSocket):
    await websocket.send_text(json.dumps({
        "type": "gruppi",
        "gruppi": [
            {
                "nome": g.nome,
                "codice": g.codice,
                "fasciaOraria_id": g.fasciaOraria_id,
                "numero_tappa": g.numero_tappa,
                "arrivato": g.arrivato,
                "orario_partenza_effettivo": g.orario_partenza_effettivo,
                "orario_fine_effettivo": g.orario_fine_effettivo,
                "percorsoFinito": g.percorsoFinito,
                "aula_nome": g.aula_nome,
                "aula_posizione": g.aula_posizione,
                "aula_materia": g.aula_materia,
                "minuti_arrivo": g.minuti_arrivo,
                "minuti_partenza": g.minuti_partenza,
                "totale_orientati": g.totale_orientati,
                "orientati_presenti": g.orientati_presenti,
                "orientati_assenti": g.orientati_assenti,
                "orario_partenza": g.orario_partenza,
                "id": g.id
            } for g in get_all_gruppi().gruppi
        ]}))