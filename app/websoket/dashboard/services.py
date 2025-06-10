import json
import logging

from fastapi import WebSocket

from ...database import get_db
from ...models import Gruppo, Iscrizione, Ragazzo, FasciaOraria, ScuolaDiProvenienza, Genitore
from ...services.admin.dashboard import gruppi
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
            } for g in gruppi.get_all_gruppi(percorso_id=percorso_id).gruppi
        ]}))


async def genera_codice_gruppo(websocket: WebSocket, gruppo_id: int):
    try:
        await websocket.send_text(json.dumps({
            "type": "codice_gruppo",
            "gruppo_id": gruppo_id,
            "codice": gruppi.genera_codice_gruppo(gruppo_id)
        }))
    except gruppi.GruppoNotFoundError as e:
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
            } for u in gruppi.get_utenti_gruppo(gruppo_id) if u is not None]
        }))
    except gruppi.GruppoNotFoundError as e:
        await websocket.send_text(json.dumps({
            "type": "error",
            "message": str(e)
        }))


async def rimuovi_utente_gruppo(websocket: WebSocket, user_id: int, group_id: int):
    try:
        gruppi.rimuovi_utente(user_id, group_id)
        await invia_utenti_gruppo(websocket, group_id)
    except (gruppi.GruppoNotFoundError, gruppi.UserNotFoundError) as e:
        await websocket.send_text(json.dumps({
            "type": "error",
            "message": str(e)
        }))


async def modifica_gruppo_iscrizione(websocket: WebSocket, group_id: int, iscrizione_id: int):
    try:
        gruppi.modifica_gruppo_iscrizione(group_id, iscrizione_id)
        await websocket.send_text(json.dumps({
            "type": "iscrizione_modificata",
            "iscrizione_id": iscrizione_id,
            "gruppo_id": group_id,
            "message": "Iscrizione modificata con successo"
        }))
    except (gruppi.GruppoNotFoundError, gruppi.IscrizioneNotFoundError) as e:
        await websocket.send_text(json.dumps({
            "type": "error",
            "message": str(e)
        }))


async def modifica_ragazzo_presente(websocket: WebSocket, ragazzo_id: int, group_id: int):
    try:
        gruppi.modifica_ragazzo_presente(ragazzo_id, group_id)
        await websocket.send_text(json.dumps({
            "type": "ragazzo_presente",
            "user_id": ragazzo_id,
            "group_id": group_id,
            "message": "Ragazzo marcato come presente"
        }))
    except (gruppi.RagazzoNotFoundError, gruppi.GruppoNotFoundError, gruppi.RagazzoAlreadyPresentError) as e:
        await websocket.send_text(json.dumps({
            "type": "error",
            "message": str(e)
        }))


async def modifica_ragazzo_assente(websocket: WebSocket, ragazzo_id: int, group_id: int):
    try:
        gruppi.modifica_ragazzo_assente(ragazzo_id, group_id)
        await websocket.send_text(json.dumps({
            "type": "ragazzo_assente",
            "user_id": ragazzo_id,
            "group_id": group_id,
            "message": "Ragazzo marcato come assente"
        }))
    except (gruppi.RagazzoNotFoundError, gruppi.GruppoNotFoundError, gruppi.RagazzoAlreadyAbsentError) as e:
        await websocket.send_text(json.dumps({
            "type": "error",
            "message": str(e)
        }))


async def modifica_ragazzo_non_arrivato(websocket: WebSocket, ragazzo_id: int, group_id: int):
    db = next(get_db())

    # Controlla se il ragazzo esiste
    ragazzo = db.query(Ragazzo).filter(Ragazzo.id == ragazzo_id).first()
    if not ragazzo:
        await websocket.send_text(json.dumps({
            "type": "error",
            "message": "Ragazzo non trovato"
        }))
        return

    # Controlla se il gruppo esiste
    gruppo = db.query(Gruppo).filter(Gruppo.id == group_id).first()
    if not gruppo:
        await websocket.send_text(json.dumps({
            "type": "error",
            "message": "Gruppo non trovato"
        }))
        return

    # Controlla se il ragazzo è iscritto al gruppo
    iscrizioni = db.query(Iscrizione).filter(Iscrizione.gruppo_id == gruppo.id).all()
    if not any(ragazzo in iscrizione.ragazzi for iscrizione in iscrizioni):
        await websocket.send_text(json.dumps({
            "type": "error",
            "message": "Ragazzo non iscritto a questo gruppo"
        }))
        return

    # Rimuove eventuali presenze o assenze precedenti del ragazzo nel gruppo
    for p in ragazzo.presenze:
        if p.gruppo_id == gruppo.id:
            db.delete(p)
            break

    # Rimuove eventuali assenze precedenti del ragazzo nel gruppo
    for a in ragazzo.assenze:
        if a.gruppo_id == gruppo.id:
            db.delete(a)
            break
    db.commit()
    db.refresh(ragazzo)

    await websocket.send_text(json.dumps({
        "type": "ragazzo_non_arrivato",
        "user_id": ragazzo_id,
        "group_id": group_id,
        "message": "Ragazzo marcato come non arrivato"
    }))


async def modifica_fascia_oraria_orario_partenza(websocket: WebSocket, fascia_oraria_id: int, orario_partenza: str):
    db = next(get_db())
    fascia_oraria = db.query(FasciaOraria).filter(FasciaOraria.id == fascia_oraria_id).first()

    # Controlla se il la fascia oraria esiste
    if not fascia_oraria:
        await websocket.send_text(json.dumps({
            "type": "error",
            "message": "Fascia oraria non trovata"
        }))
        return

    # Controlla se l'orario di partenza è valido
    try:
        orario_partenza = orario_partenza.strip()
        if not orario_partenza:
            raise ValueError("Orario di partenza non può essere vuoto")
    except ValueError as e:
        await websocket.send_text(json.dumps({
            "type": "error",
            "message": str(e)
        }))
        return

    # Aggiorna l'orario di partenza della fascia oraria
    fascia_oraria.oraInizio = orario_partenza
    db.commit()
    db.refresh(fascia_oraria)
    await websocket.send_text(json.dumps({
        "type": "fascia_oraria_modificata",
        "fascia_oraria_id": fascia_oraria_id,
        "orario_partenza": orario_partenza,
        "message": "Orario di partenza della fascia oraria modificato con successo"
    }))


async def modifica_gruppo_nome(websocket: WebSocket, group_id: int, new_name: str):
    db = next(get_db())
    gruppo = db.query(Gruppo).filter(Gruppo.id == group_id).first()

    # Controlla se il gruppo esiste
    if not gruppo:
        await websocket.send_text(json.dumps({
            "type": "error",
            "message": "Gruppo non trovato"
        }))
        return

    # Controlla se il nuovo nome è valido
    if not new_name or len(new_name.strip()) == 0:
        await websocket.send_text(json.dumps({
            "type": "error",
            "message": "Il nome del gruppo non può essere vuoto"
        }))
        return

    # Aggiorna il nome del gruppo
    gruppo.nome = new_name.strip()
    db.commit()
    db.refresh(gruppo)
    await websocket.send_text(json.dumps({
        "type": "gruppo_modificato",
        "group_id": group_id,
        "new_name": new_name,
        "message": "Nome del gruppo modificato con successo"
    }))


async def modifica_gruppo_tappa(websocket: WebSocket, group_id: int, numero_tappa: int, arrivato: str):
    db = next(get_db())
    gruppo = db.query(Gruppo).filter(Gruppo.id == group_id).first()

    # Controlla se il gruppo esiste
    if not gruppo:
        await websocket.send_text(json.dumps({
            "type": "error",
            "message": "Gruppo non trovato"
        }))
        return

    arrivato = arrivato.lower() == 'true'  # Converte la stringa in booleano

    # Aggiorna il numero della tappa e lo stato di arrivo del gruppo
    gruppo.numero_tappa = numero_tappa
    gruppo.arrivato = arrivato
    db.commit()
    db.refresh(gruppo)

    await websocket.send_text(json.dumps({
        "type": "gruppo_tappa_modificata",
        "group_id": group_id,
        "numero_tappa": numero_tappa,
        "arrivato": arrivato,
        "message": "Tappa del gruppo modificata con successo"
    }))


async def crea_ragazzo_gruppo(websocket: WebSocket, group_id: int, name: str, surname: str,
                              scuolaDiProvenienza_id: int = None, genitore_id: int = None):
    db = next(get_db())
    gruppo = db.query(Gruppo).filter(Gruppo.id == group_id).first()

    if not name or not surname:
        await websocket.send_text(json.dumps({
            "type": "error",
            "message": "Nome e cognome sono obbligatori"
        }))
        return

    if not gruppo:
        await websocket.send_text(json.dumps({
            "type": "error",
            "message": "Gruppo non trovato"
        }))
        return

    ragazzo = Ragazzo(nome=name, cognome=surname, scuolaDiProvenienza_id=scuolaDiProvenienza_id,
                      genitore_id=genitore_id)
    db.add(ragazzo)
    db.commit()
    db.refresh(ragazzo)

    iscrizione = Iscrizione(gruppo_id=gruppo.id, genitore_id=genitore_id, fasciaOraria_id=gruppo.fasciaOraria_id)
    db.add(iscrizione)
    db.commit()
    db.refresh(iscrizione)

    iscrizione.ragazzi.append(ragazzo)
    db.commit()
    db.refresh(iscrizione)

    await websocket.send_text(json.dumps({
        "type": "ragazzo_creato",
        "ragazzo_id": ragazzo.id,
        "group_id": group_id,
        "iscrizione_id": iscrizione.id,
        "message": f"Ragazzo {name} {surname} creato e aggiunto al gruppo"
    }))


async def crea_ragazzo_iscrizione(websocket: WebSocket, iscrizione_id: int, name: str, surname: str,
                                  scuolaDiProvenienza_id: int = None):
    db = next(get_db())
    iscrizione = db.query(Iscrizione).filter(Iscrizione.id == iscrizione_id).first()

    if not name or not surname:
        await websocket.send_text(json.dumps({
            "type": "error",
            "message": "Nome e cognome sono obbligatori"
        }))
        return

    if not iscrizione:
        await websocket.send_text(json.dumps({
            "type": "error",
            "message": "Iscrizione non trovata"
        }))
        return

    ragazzo = Ragazzo(nome=name, cognome=surname, scuolaDiProvenienza_id=scuolaDiProvenienza_id,
                      genitore_id=iscrizione.genitore_id)
    db.add(ragazzo)
    db.commit()
    db.refresh(ragazzo)

    iscrizione.ragazzi.append(ragazzo)
    db.commit()
    db.refresh(iscrizione)

    await websocket.send_text(json.dumps({
        "type": "ragazzo_creato",
        "ragazzo_id": ragazzo.id,
        "iscrizione_id": iscrizione.id,
        "message": f"Ragazzo {name} {surname} creato e aggiunto all'iscrizione"
    }))


async def get_scuole_di_provenienza(websocket: WebSocket):
    db = next(get_db())
    scuole = db.query(ScuolaDiProvenienza).distinct().all()

    scuole_list = [{"id": scuola.id, "nome": scuola.nome} for scuola in scuole if scuola is not None]

    await websocket.send_text(json.dumps({
        "type": "scuole_di_provenienza",
        "scuole": scuole_list
    }))


async def get_genitori(websocket: WebSocket):
    db = next(get_db())
    genitori = db.query(Genitore).distinct().all()

    genitori_list = [{"id": genitore.id, "nome": genitore.nome, "cognome": genitore.cognome} for genitore in genitori if
                     genitore is not None]

    await websocket.send_text(json.dumps({
        "type": "genitori",
        "genitori": genitori_list
    }))


async def get_ragazzi(websocket: WebSocket):
    db = next(get_db())
    ragazzi = db.query(Ragazzo).distinct().all()

    ragazzi_list = [{
        "id": ragazzo.id,
        "nome": ragazzo.nome,
        "cognome": ragazzo.cognome,
        "scuolaDiProvenienza_id": ragazzo.scuolaDiProvenienza_id if ragazzo.scuolaDiProvenienza else None,
        "genitore_id": ragazzo.genitore_id if ragazzo.genitore else None,
    } for ragazzo in ragazzi if ragazzo is not None]

    await websocket.send_text(json.dumps({
        "type": "ragazzi",
        "ragazzi": ragazzi_list
    }))


async def collega_ragazzo_iscrizione(websocket: WebSocket, ragazzo_id: int, iscrizione_id: int):
    db = next(get_db())
    ragazzo = db.query(Ragazzo).filter(Ragazzo.id == ragazzo_id).first()
    iscrizione = db.query(Iscrizione).filter(Iscrizione.id == iscrizione_id).first()

    if not ragazzo:
        await websocket.send_text(json.dumps({
            "type": "error",
            "message": "Ragazzo non trovato"
        }))
        return

    if not iscrizione:
        await websocket.send_text(json.dumps({
            "type": "error",
            "message": "Iscrizione non trovata"
        }))
        return

    if ragazzo in iscrizione.ragazzi:
        await websocket.send_text(json.dumps({
            "type": "error",
            "message": "Ragazzo già collegato a questa iscrizione"
        }))
        return

    iscrizione.ragazzi.append(ragazzo)
    db.commit()
    db.refresh(iscrizione)

    await websocket.send_text(json.dumps({
        "type": "ragazzo_collegato",
        "ragazzo_id": ragazzo.id,
        "iscrizione_id": iscrizione.id,
        "message": f"Ragazzo {ragazzo.nome} {ragazzo.cognome} collegato all'iscrizione con successo"
    }))
