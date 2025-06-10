from datetime import datetime

from app.database import get_db, get_db_context
from app.models import Gruppo, Presente, Assente, FasciaOraria, Data, Utente, Iscrizione
from app.schemas.admin.dashboard.gruppo import GruppoList, GruppoResponse
from app.services.admin.gruppo import crea_codice_gruppo


class GruppoNotFoundError(Exception):
    """Eccezione sollevata quando un gruppo non viene trovato nel database."""
    pass


class UserNotFoundError(Exception):
    """Eccezione sollevata quando un utente non viene trovato nel database."""
    pass


class IscrizioneNotFoundError(Exception):
    """Eccezione sollevata quando un'iscrizione non viene trovata nel database."""
    pass


def get_all_gruppi(percorso_id: int = None):
    """
    Legge tutti i gruppi del giorno dal database
    """
    db = next(get_db())

    gruppi = db.query(Gruppo).join(Gruppo.fasciaOraria).join(FasciaOraria.data).filter(
        Data.data == datetime.now().strftime("%Y-%m-%d"),
        FasciaOraria.percorso_id == percorso_id
    ).all()
    # ordino i gruppi per fascia oraria
    gruppi = sorted(gruppi, key=lambda gruppo: gruppo.fasciaOraria.oraInizio)
    listaGruppi = GruppoList(gruppi=[])
    if not gruppi:
        db.close()
        return listaGruppi

    listaGruppi.gruppi = [GruppoResponse.model_validate(gruppo) for gruppo in gruppi]
    for gruppo in listaGruppi.gruppi:
        db_gruppo = db.query(Gruppo).join(Gruppo.fasciaOraria).filter(Gruppo.id == gruppo.id).first()

        if db_gruppo.numero_tappa == 0 and db_gruppo.arrivato:
            gruppo.percorsoFinito = True

        if not gruppo.numero_tappa == 0:
            tappe = sorted(db_gruppo.fasciaOraria.percorso.tappe, key=lambda tappa: tappa.minuti_partenza)
            if gruppo.numero_tappa == 0:
                gruppo.aula_nome = ""
                gruppo.aula_posizione = ""
                gruppo.aula_materia = ""
                gruppo.minuti_arrivo = 0
                gruppo.minuti_partenza = 0
            else:
                gruppo.aula_nome = tappe[gruppo.numero_tappa - 1].aula.nome
                gruppo.aula_posizione = tappe[gruppo.numero_tappa - 1].aula.posizione
                gruppo.aula_materia = tappe[gruppo.numero_tappa - 1].aula.materia
                gruppo.minuti_arrivo = tappe[gruppo.numero_tappa - 1].minuti_arrivo
                gruppo.minuti_partenza = tappe[gruppo.numero_tappa - 1].minuti_partenza

        gruppo.orario_partenza = db_gruppo.fasciaOraria.oraInizio

        iscrizioni = db.query(Gruppo).filter(Gruppo.id == gruppo.id).first().iscrizioni
        ragazzi = [ragazzo for iscrizione in iscrizioni for ragazzo in iscrizione.ragazzi]
        gruppo.totale_orientati = len(ragazzi)
        presenti = db.query(Presente).filter(Presente.gruppo_id == gruppo.id).all()
        gruppo.orientati_presenti = len(presenti)
        assenti = db.query(Assente).filter(Assente.gruppo_id == gruppo.id).all()
        gruppo.orientati_assenti = len(assenti)

    listaGruppi.gruppi = sorted(listaGruppi.gruppi,
                                key=lambda gruppo: (gruppo.percorsoFinito is True, gruppo.orario_partenza))
    db.close()
    return listaGruppi


def genera_codice_gruppo(gruppo_id: int):
    """
    Genera un nuovo codice per il gruppo specificato e lo restituisce.
    """
    db = next(get_db())

    if not db.query(Gruppo).filter(Gruppo.id == gruppo_id).first():
        raise GruppoNotFoundError(f"Gruppo con ID {gruppo_id} non trovato.")
    gruppo = db.query(Gruppo).filter(Gruppo.id == gruppo_id).first()
    gruppo.codice = crea_codice_gruppo()
    db.commit()
    db.refresh(gruppo)
    db.close()
    return gruppo.codice


def get_utenti_gruppo(gruppo_id: int):
    """
    Restituisce gli utenti di un gruppo
    """
    db = next(get_db())
    gruppo = db.query(Gruppo).filter(Gruppo.id == gruppo_id).first()
    if not gruppo:
        db.close()
        raise GruppoNotFoundError(f"Gruppo con ID {gruppo_id} non trovato.")

    utenti = list(gruppo.utenti)
    db.close()
    if not utenti:
        return []

    return utenti


def rimuovi_utente(user_id: int, group_id: int):
    db = next(get_db())
    gruppo = db.query(Gruppo).filter(Gruppo.id == group_id).first()
    if not gruppo:
        db.close()
        raise GruppoNotFoundError(f"Gruppo con ID {group_id} non trovato.")

    utente = db.query(Utente).filter(Utente.id == user_id, Utente.gruppo_id == group_id).first()

    if not utente:
        db.close()
        raise UserNotFoundError(f"Utente con ID {user_id} non trovato nel gruppo {group_id}.")

    gruppo.utenti.remove(utente)
    db.commit()
    db.refresh(gruppo)
    db.close()
    return gruppo


def modifica_gruppo_iscrizione(group_id, iscrizione_id):
    with get_db_context() as db:
        gruppo = db.query(Gruppo).filter(Gruppo.id == group_id).first()
        if not gruppo:
            raise GruppoNotFoundError(f"Gruppo con ID {group_id} non trovato.")
        iscrizione = db.query(Iscrizione).filter(Iscrizione.id == iscrizione_id).first()
        if not iscrizione:
            raise IscrizioneNotFoundError(f"Iscrizione con ID {iscrizione_id} non trovata.")

        iscrizione.gruppo_id = group_id
        db.commit()
        db.refresh(iscrizione)
        return iscrizione
