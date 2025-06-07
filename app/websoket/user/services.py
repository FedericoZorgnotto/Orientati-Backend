import json
import logging

from fastapi import WebSocket

from ..enums import UserRole
from ..models import ConnectedUser
from ...services.orientatore.gruppo import get_gruppo_utente, get_gruppo

logger = logging.getLogger(__name__)


async def invia_user_gruppo(user: ConnectedUser, websocket: WebSocket):
    gruppo_utente = None
    try:
        gruppo_id = get_gruppo_utente(user.id)
        if gruppo_id is None:
            raise ValueError("Gruppo non trovato per l'utente")
        gruppo_utente = get_gruppo(gruppo_id)
    except Exception as e:
        await websocket.send_text(json.dumps({
            "type": "error",
            "message": "Errore nel recupero del gruppo"
        }))
        logger.error(f"Errore nel recupero del gruppo per l'utente {user.id}: {str(e)}")
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
            "gruppo_partito": gruppo_utente.gruppo_partito,
            "percorso_finito": gruppo_utente.percorso_finito,
            "orientati_presenti": gruppo_utente.orientati_presenti,
            "orientati_assenti": gruppo_utente.orientati_assenti,
            "orientati_totali": gruppo_utente.orientati_totali,
            "tappa": {
                "minuti_arrivo": gruppo_utente.tappa.minuti_arrivo,
                "minuti_partenza": gruppo_utente.tappa.minuti_partenza,
                "ora_ingresso": gruppo_utente.tappa.ora_ingresso,
                "aula": {
                    "nome": gruppo_utente.tappa.aula.nome,
                    "posizione": gruppo_utente.tappa.aula.posizione,
                    "materia": gruppo_utente.tappa.aula.materia,
                    "dettagli": gruppo_utente.tappa.aula.dettagli,
                }
            },
            "tappa_successiva": {
                "minuti_arrivo": gruppo_utente.tappa_successiva.minuti_arrivo if gruppo_utente.tappa_successiva else None,
                "minuti_partenza": gruppo_utente.tappa_successiva.minuti_partenza if gruppo_utente.tappa_successiva else None,
                "occupata": gruppo_utente.tappa_successiva.occupata if gruppo_utente.tappa_successiva else None,
                "aula": {
                    "nome": gruppo_utente.tappa_successiva.aula.nome if gruppo_utente.tappa_successiva else None,
                    "posizione": gruppo_utente.tappa_successiva.aula.posizione if gruppo_utente.tappa_successiva else None,
                    "materia": gruppo_utente.tappa_successiva.aula.materia if gruppo_utente.tappa_successiva else None,
                    "dettagli": gruppo_utente.tappa_successiva.aula.dettagli if gruppo_utente.tappa_successiva else None,
                }
            } if gruppo_utente.tappa_successiva else None
        }
    }))


async def invia_users_gruppo(gruppo_id, websocket_manager):
    # esegue invia_user_gruppo per tutti gli utenti che sono connessi al gruppo, in base al campo gruppo_id del ConnectedUser
    for role, connections in websocket_manager.active_connections.items():
        for conn in connections.values():
            if conn.group_id == gruppo_id and conn.role == UserRole.USER:
                await invia_user_gruppo(conn.user, conn.websocket)
