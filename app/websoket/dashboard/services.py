import json
import logging

from fastapi import WebSocket

from ...database import get_db
from ...models import Gruppo
from ...services.admin.dashboard.aule import get_all_aule
from ...services.admin.dashboard.gruppi import get_all_gruppi
from ...services.admin.dashboard.orientati import get_all_orientati
from ...services.admin.gruppo import crea_codice_gruppo

logger = logging.getLogger(__name__)


async def invia_admin_aule(websocket: WebSocket, percorso_id: int = None):
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
        } for a in get_all_aule(percorso_id=percorso_id).aule]
    }))


async def invia_admin_orientati(websocket: WebSocket, percorso_id: int):
    await websocket.send_text(json.dumps(
        {"type": "orientati",
         "iscrizioni":
             [{
                 "genitore_id": iscrizione.genitore_id,
                 "genitore_nome": iscrizione.genitore_nome,
                 "genitore_cognome": iscrizione.genitore_cognome,
                 "gruppo_id": iscrizione.gruppo_id,
                 "gruppo_nome": iscrizione.gruppo_nome,
                 "gruppo_orario_partenza": iscrizione.gruppo_orario_partenza,
                 "fascia_oraria_id": iscrizione.fascia_oraria_id,
                 "orientati": [
                     {"id": o.id,
                      "nome": o.nome,
                      "cognome": o.cognome,
                      "scuolaDiProvenienza_id": o.scuolaDiProvenienza_id,
                      "scuolaDiProvenienza_nome": o.scuolaDiProvenienza_nome,
                      "presente": o.presente,
                      "assente": o.assente
                      } for o in iscrizione.orientati
                 ]} for iscrizione in get_all_orientati(percorso_id=percorso_id).iscrizioni
             ]}))


async def invia_admin_gruppi(websocket: WebSocket, percorso_id: int = None):
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
            } for g in get_all_gruppi(percorso_id=percorso_id).gruppi
        ]}))


async def genera_codice_gruppo(websocket: WebSocket, gruppo_id: int):
    db = next(get_db())

    if not db.query(Gruppo).filter(Gruppo.id == gruppo_id).first():
        raise Exception("Gruppo not found")
    gruppo = db.query(Gruppo).filter(Gruppo.id == gruppo_id).first()
    gruppo.codice = crea_codice_gruppo()
    db.commit()
    db.refresh(gruppo)
    await websocket.send_text(json.dumps({
        "type": "codice_gruppo",
        "gruppo_id": gruppo.id,
        "codice": gruppo.codice
    }))


async def invia_utenti_gruppo(websocket: WebSocket, gruppo_id: int):
    db = next(get_db())
    gruppo = db.query(Gruppo).filter(Gruppo.id == gruppo_id).first()

    if not gruppo:
        await websocket.send_text(json.dumps({
            "type": "error",
            "message": "Gruppo non trovato"
        }))
        return

    utenti = [{
        "id": u.id,
        "username": u.username,
        "temporaneo": u.temporaneo,
    } for u in gruppo.utenti]

    await websocket.send_text(json.dumps({
        "type": "utenti_gruppo",
        "gruppo_id": gruppo.id,
        "utenti": utenti
    }))


async def rimuovi_utente_gruppo(websocket: WebSocket, user_id: int, group_id: int):
    db = next(get_db())
    gruppo = db.query(Gruppo).filter(Gruppo.id == group_id).first()

    if not gruppo:
        await websocket.send_text(json.dumps({
            "type": "error",
            "message": "Gruppo non trovato"
        }))
        return

    utente = next((u for u in gruppo.utenti if u.id == int(user_id)), None)

    if not utente:
        await websocket.send_text(json.dumps({
            "type": "error",
            "message": "Utente non trovato nel gruppo"
        }))
        return

    gruppo.utenti.remove(utente)
    db.commit()
    db.refresh(gruppo)

    await invia_utenti_gruppo(websocket, group_id)
