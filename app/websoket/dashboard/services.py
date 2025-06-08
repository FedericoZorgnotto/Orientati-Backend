import json
import logging

from fastapi import WebSocket

from ...database import get_db
from ...models import Gruppo, Iscrizione, Ragazzo, Presente, Assente, FasciaOraria
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


async def modifica_iscrizione_gruppo(websocket: WebSocket, group_id: int, iscrizione_id: int):
    db = next(get_db())
    gruppo = db.query(Gruppo).filter(Gruppo.id == group_id).first()

    if not gruppo:
        await websocket.send_text(json.dumps({
            "type": "error",
            "message": "Gruppo non trovato"
        }))
        return

    iscrizione = db.query(Iscrizione).filter(Iscrizione.id == iscrizione_id).first()
    if not iscrizione:
        await websocket.send_text(json.dumps({
            "type": "error",
            "message": "Iscrizione non trovata"
        }))
        return

    iscrizione.gruppo_id = group_id
    db.commit()
    db.refresh(iscrizione)
    await websocket.send_text(json.dumps({
        "type": "iscrizione_modificata",
        "iscrizione_id": iscrizione.id,
        "gruppo_id": group_id,
        "message": "Iscrizione modificata con successo"
    }))


async def modifica_ragazzo_presente(websocket: WebSocket, user_id: int, group_id: int):
    db = next(get_db())

    # Controlla se il ragazzo esiste
    ragazzo = db.query(Ragazzo).filter(Ragazzo.id == user_id).first()
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
    for a in ragazzo.assenze:
        if a.gruppo_id == gruppo.id:
            db.delete(a)
            break

    # Controlla se il ragazzo è già presente nel gruppo
    for p in ragazzo.presenze:
        if p.gruppo_id == gruppo.id:
            await websocket.send_text(json.dumps({
                "type": "error",
                "message": "Ragazzo già presente in questo gruppo"
            }))
            return

    # Aggiunge la presenza del ragazzo al gruppo
    ragazzo.presenze.append(Presente(
        ragazzo_id=ragazzo.id,
        gruppo_id=gruppo.id
    ))
    db.commit()
    db.refresh(ragazzo)
    await websocket.send_text(json.dumps({
        "type": "ragazzo_presente",
        "user_id": user_id,
        "group_id": group_id,
        "message": "Ragazzo marcato come presente"
    }))


async def modifica_ragazzo_assente(websocket: WebSocket, user_id: int, group_id: int):
    db = next(get_db())

    # Controlla se il ragazzo esiste
    ragazzo = db.query(Ragazzo).filter(Ragazzo.id == user_id).first()
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

    # Rimuove eventuali presenze precedenti del ragazzo nel gruppo
    for p in ragazzo.presenze:
        if p.gruppo_id == gruppo.id:
            db.delete(p)
            break

    # Controlla se il ragazzo è già assente nel gruppo
    for a in ragazzo.assenze:
        if a.gruppo_id == gruppo.id:
            await websocket.send_text(json.dumps({
                "type": "error",
                "message": "Ragazzo già assente in questo gruppo"
            }))
            return

    # Aggiunge l'assenza del ragazzo al gruppo
    ragazzo.assenze.append(Assente(
        ragazzo_id=ragazzo.id,
        gruppo_id=gruppo.id
    ))
    db.commit()
    db.refresh(ragazzo)
    await websocket.send_text(json.dumps({
        "type": "ragazzo_assente",
        "user_id": user_id,
        "group_id": group_id,
        "message": "Ragazzo marcato come assente"
    }))


async def modifica_ragazzo_non_arrivato(websocket: WebSocket, user_id: int, group_id: int):
    db = next(get_db())

    # Controlla se il ragazzo esiste
    ragazzo = db.query(Ragazzo).filter(Ragazzo.id == user_id).first()
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
        "user_id": user_id,
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


