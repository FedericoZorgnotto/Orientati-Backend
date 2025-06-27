import json
import logging

from fastapi import WebSocket

from ...services.admin.dashboard import gruppi as Gruppi, scuoleDiProvenienza as ScuoleDiProvenienza, \
    genitori as Genitori, ragazzi as Ragazzi
from ...services.admin.dashboard.aule import get_all_aule
from ...services.admin.dashboard.orientati import get_all_orientati

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
            } for g in Gruppi.get_all_gruppi(percorso_id=percorso_id).gruppi
        ]}))


async def genera_codice_gruppo(websocket: WebSocket, gruppo_id: int):
    try:
        await websocket.send_text(json.dumps({
            "type": "codice_gruppo",
            "gruppo_id": gruppo_id,
            "codice": Gruppi.genera_codice_gruppo(gruppo_id)
        }))
    except Gruppi.GruppoNotFoundError as e:
        await websocket.send_text(json.dumps({
            "type": "error",
            "message": str(e)
        }))


async def invia_utenti_gruppo(websocket: WebSocket, gruppo_id: int):
    try:
        await websocket.send_text(json.dumps({
            "type": "utenti_gruppo",
            "gruppo_id": gruppo_id,
            "utenti": [{
                "id": u.id,
                "username": u.username,
                "temporaneo": u.temporaneo,
            } for u in Gruppi.get_utenti_gruppo(gruppo_id) if u is not None]
        }))
    except Gruppi.GruppoNotFoundError as e:
        await websocket.send_text(json.dumps({
            "type": "error",
            "message": str(e)
        }))


async def rimuovi_utente_gruppo(websocket: WebSocket, user_id: int, group_id: int):
    try:
        Gruppi.rimuovi_utente(user_id, group_id)
        await invia_utenti_gruppo(websocket, group_id)
    except (Gruppi.GruppoNotFoundError, Gruppi.UserNotFoundError) as e:
        await websocket.send_text(json.dumps({
            "type": "error",
            "message": str(e)
        }))


async def modifica_gruppo_iscrizione(websocket: WebSocket, group_id: int, iscrizione_id: int):
    try:
        Gruppi.modifica_gruppo_iscrizione(group_id, iscrizione_id)
        await websocket.send_text(json.dumps({
            "type": "iscrizione_modificata",
            "iscrizione_id": iscrizione_id,
            "gruppo_id": group_id,
            "message": "Iscrizione modificata con successo"
        }))
    except (Gruppi.GruppoNotFoundError, Gruppi.IscrizioneNotFoundError) as e:
        await websocket.send_text(json.dumps({
            "type": "error",
            "message": str(e)
        }))


async def modifica_ragazzo_presente(websocket: WebSocket, ragazzo_id: int, group_id: int):
    try:
        Gruppi.modifica_ragazzo_presente(ragazzo_id, group_id)
        await websocket.send_text(json.dumps({
            "type": "ragazzo_presente",
            "user_id": ragazzo_id,
            "group_id": group_id,
            "message": "Ragazzo marcato come presente"
        }))
    except (Gruppi.RagazzoNotFoundError, Gruppi.GruppoNotFoundError, Gruppi.RagazzoAlreadyPresentError) as e:
        await websocket.send_text(json.dumps({
            "type": "error",
            "message": str(e)
        }))


async def modifica_ragazzo_assente(websocket: WebSocket, ragazzo_id: int, group_id: int):
    try:
        Gruppi.modifica_ragazzo_assente(ragazzo_id, group_id)
        await websocket.send_text(json.dumps({
            "type": "ragazzo_assente",
            "user_id": ragazzo_id,
            "group_id": group_id,
            "message": "Ragazzo marcato come assente"
        }))
    except (Gruppi.RagazzoNotFoundError, Gruppi.GruppoNotFoundError, Gruppi.RagazzoAlreadyAbsentError) as e:
        await websocket.send_text(json.dumps({
            "type": "error",
            "message": str(e)
        }))


async def modifica_ragazzo_non_arrivato(websocket: WebSocket, ragazzo_id: int, group_id: int):
    try:
        Gruppi.modifica_ragazzo_non_arrivato(ragazzo_id, group_id)
        await websocket.send_text(json.dumps({
            "type": "ragazzo_non_arrivato",
            "user_id": ragazzo_id,
            "group_id": group_id,
            "message": "Ragazzo marcato come non arrivato"
        }))
    except (Gruppi.RagazzoNotFoundError, Gruppi.GruppoNotFoundError) as e:
        await websocket.send_text(json.dumps({
            "type": "error",
            "message": str(e)
        }))


async def modifica_fascia_oraria_orario_partenza(websocket: WebSocket, fascia_oraria_id: int, orario_partenza: str):
    try:
        Gruppi.modifica_fascia_oraria_orario_partenza(fascia_oraria_id, orario_partenza)
        await websocket.send_text(json.dumps({
            "type": "fascia_oraria_modificata",
            "fascia_oraria_id": fascia_oraria_id,
            "orario_partenza": orario_partenza,
            "message": "Orario di partenza della fascia oraria modificato con successo"
        }))
    except (Gruppi.FasciaOrariaNotFoundError, Gruppi.GruppoNotFoundError) as e:
        await websocket.send_text(json.dumps({
            "type": "error",
            "message": str(e)
        }))


async def modifica_gruppo_nome(websocket: WebSocket, group_id: int, new_name: str):
    try:
        Gruppi.modifica_gruppo_nome(group_id, new_name)
        await websocket.send_text(json.dumps({
            "type": "gruppo_modificato",
            "group_id": group_id,
            "new_name": new_name,
            "message": "Nome del gruppo modificato con successo"
        }))
    except (Gruppi.GruppoNotFoundError, Gruppi.InvalidGroupNameError) as e:
        await websocket.send_text(json.dumps({
            "type": "error",
            "message": str(e)
        }))


async def modifica_gruppo_tappa(websocket: WebSocket, group_id: int, numero_tappa: int, arrivato: str):
    try:
        arrivato = arrivato.strip().lower() == "true"
        Gruppi.modifica_gruppo_tappa(group_id, numero_tappa, arrivato)
        await websocket.send_text(json.dumps({
            "type": "gruppo_tappa_modificata",
            "group_id": group_id,
            "numero_tappa": numero_tappa,
            "arrivato": arrivato,
            "message": "Tappa del gruppo modificata con successo"
        }))
    except (Gruppi.GruppoNotFoundError, Gruppi.InvalidTappaNumberError) as e:
        await websocket.send_text(json.dumps({
            "type": "error",
            "message": str(e)
        }))


async def crea_ragazzo_gruppo(websocket: WebSocket, group_id: int, name: str, surname: str,
                              scuolaDiProvenienza_id: int = None, genitore_id: int = None):
    try:
        ragazzo, iscrizione = Gruppi.crea_ragazzo_gruppo(group_id, name, surname, scuolaDiProvenienza_id, genitore_id)
        await websocket.send_text(json.dumps({
            "type": "ragazzo_creato",
            "group_id": group_id,
            "name": name,
            "surname": surname,
            "scuolaDiProvenienza_id": scuolaDiProvenienza_id if scuolaDiProvenienza_id else None,
            "genitore_id": genitore_id if genitore_id else None,
            "iscrizione_id": iscrizione.id,
            "message": f"Ragazzo {name} {surname} creato e aggiunto al gruppo"
        }))
    except (Gruppi.GruppoNotFoundError, Gruppi.InvalidRagazzoDataError) as e:
        await websocket.send_text(json.dumps({
            "type": "error",
            "message": str(e)
        }))


async def crea_ragazzo_iscrizione(websocket: WebSocket, iscrizione_id: int, name: str, surname: str,
                                  scuolaDiProvenienza_id: int = None):
    try:
        ragazzo, iscrizione = Gruppi.crea_ragazzo_iscrizione(iscrizione_id, name, surname, scuolaDiProvenienza_id)
        await websocket.send_text(json.dumps({
            "type": "ragazzo_creato_iscrizione",
            "iscrizione_id": iscrizione.id,
            "name": name,
            "surname": surname,
            "scuolaDiProvenienza_id": scuolaDiProvenienza_id if scuolaDiProvenienza_id else None,
            "message": f"Ragazzo {name} {surname} creato e aggiunto all'iscrizione"
        }))
    except (Gruppi.IscrizioneNotFoundError, Gruppi.InvalidRagazzoDataError) as e:
        await websocket.send_text(json.dumps({
            "type": "error",
            "message": str(e)
        }))


async def get_scuole_di_provenienza(websocket: WebSocket):
    scuole = ScuoleDiProvenienza.get_all_scuole()
    scuole_list = [{"id": scuola.id, "nome": scuola.nome} for scuola in scuole if scuola is not None]
    await websocket.send_text(json.dumps({
        "type": "scuole_di_provenienza",
        "scuole": scuole_list
    }))


async def get_genitori(websocket: WebSocket):
    genitori = Genitori.get_all_genitori()
    genitori_list = [{
        "id": genitore.id,
        "nome": genitore.nome,
        "cognome": genitore.cognome
    } for genitore in genitori if genitore is not None]
    await websocket.send_text(json.dumps({
        "type": "genitori",
        "genitori": genitori_list
    }))


async def get_ragazzi(websocket: WebSocket):
    ragazzi = Ragazzi.get_all_ragazzi()
    ragazzi_list = [{
        "id": ragazzo.id,
        "nome": ragazzo.nome,
        "cognome": ragazzo.cognome,
        "scuolaDiProvenienza_id": ragazzo.scuolaDiProvenienza_id if ragazzo.scuolaDiProvenienza_id else None,
        "genitore_id": ragazzo.genitore_id if ragazzo.genitore_id else None,
    } for ragazzo in ragazzi if ragazzo is not None]
    await websocket.send_text(json.dumps({
        "type": "ragazzi",
        "ragazzi": ragazzi_list
    }))


async def collega_ragazzo_iscrizione(websocket: WebSocket, ragazzo_id: int, iscrizione_id: int):
    try:
        Gruppi.collega_ragazzo_iscrizione(ragazzo_id, iscrizione_id)
        await websocket.send_text(json.dumps({
            "type": "ragazzo_collegato",
            "ragazzo_id": ragazzo_id,
            "iscrizione_id": iscrizione_id,
            "message": f"Ragazzo collegato all'iscrizione con successo"
        }))
    except (Gruppi.RagazzoNotFoundError, Gruppi.IscrizioneNotFoundError, Gruppi.RagazzoAlreadyLinkedError) as e:
        await websocket.send_text(json.dumps({
            "type": "error",
            "message": str(e)
        }))
