from datetime import datetime

from app.database import get_db, get_db_context
from app.models import Gruppo, Presente, Assente, FasciaOraria, Data, Utente, Iscrizione, Ragazzo, Percorso
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


class RagazzoNotFoundError(Exception):
    """Eccezione sollevata quando un ragazzo non viene trovato nel database."""
    pass


class RagazzoAlreadyPresentError(Exception):
    """Eccezione sollevata quando un ragazzo è già presente in un gruppo."""
    pass


class RagazzoAlreadyAbsentError(Exception):
    """Eccezione sollevata quando un ragazzo è già assente in un gruppo."""
    pass


class FasciaOrariaNotFoundError(Exception):
    """Eccezione sollevata quando una fascia oraria non viene trovata nel database."""
    pass


class InvalidGroupNameError(Exception):
    """Eccezione sollevata quando il nome del gruppo non è valido."""
    pass


class InvalidTappaNumberError(Exception):
    """Eccezione sollevata quando il numero di tappa non è valido."""
    pass


class InvalidRagazzoDataError(Exception):
    """Eccezione sollevata quando i dati del ragazzo non sono validi."""
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


def modifica_gruppo_iscrizione(group_id: int, iscrizione_id: int):
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


def modifica_ragazzo_presente(ragazzo_id: int, group_id: int):
    with get_db_context() as db:
        ragazzo = db.query(Ragazzo).filter(Ragazzo.id == ragazzo_id).first()
        if not ragazzo:
            raise RagazzoNotFoundError(f"Ragazzo con ID {ragazzo_id} non trovato.")

        gruppo = db.query(Gruppo).filter(Gruppo.id == group_id).first()
        if not gruppo:
            raise GruppoNotFoundError(f"Gruppo con ID {group_id} non trovato.")

        # Controlla se il ragazzo è iscritto al gruppo
        iscrizioni = db.query(Iscrizione).filter(Iscrizione.gruppo_id == gruppo.id).all()
        if not any(ragazzo.id == r.id for iscrizione in iscrizioni for r in iscrizione.ragazzi):
            raise RagazzoNotFoundError(f"Ragazzo con ID {ragazzo_id} non iscritto a questo gruppo.")

        # Rimuove eventuali presenze o assenze precedenti del ragazzo nel gruppo
        for a in ragazzo.assenze:
            if a.gruppo_id == gruppo.id:
                db.delete(a)
                break

        # Controlla se il ragazzo è già presente nel gruppo
        for p in ragazzo.presenze:
            if p.gruppo_id == gruppo.id:
                raise RagazzoAlreadyPresentError(f"Ragazzo con ID {ragazzo_id} già presente in questo gruppo.")
        # Aggiunge la presenza del ragazzo al gruppo
        ragazzo.presenze.append(Presente(
            ragazzo_id=ragazzo.id,
            gruppo_id=gruppo.id
        ))
        db.commit()
        db.refresh(ragazzo)


def modifica_ragazzo_assente(ragazzo_id: int, group_id: int):
    with get_db_context() as db:
        ragazzo = db.query(Ragazzo).filter(Ragazzo.id == ragazzo_id).first()
        if not ragazzo:
            raise RagazzoNotFoundError(f"Ragazzo con ID {ragazzo_id} non trovato.")

        gruppo = db.query(Gruppo).filter(Gruppo.id == group_id).first()
        if not gruppo:
            raise GruppoNotFoundError(f"Gruppo con ID {group_id} non trovato.")

        # Controlla se il ragazzo è iscritto al gruppo
        iscrizioni = db.query(Iscrizione).filter(Iscrizione.gruppo_id == gruppo.id).all()
        if not any(ragazzo.id == r.id for iscrizione in iscrizioni for r in iscrizione.ragazzi):
            raise RagazzoNotFoundError(f"Ragazzo con ID {ragazzo_id} non iscritto a questo gruppo.")

        # Rimuove eventuali presenze precedenti del ragazzo nel gruppo
        for p in ragazzo.presenze:
            if p.gruppo_id == gruppo.id:
                db.delete(p)
                break

        # Controlla se il ragazzo è già assente nel gruppo
        for a in ragazzo.assenze:
            if a.gruppo_id == gruppo.id:
                raise RagazzoAlreadyAbsentError(f"Ragazzo con ID {ragazzo_id} già assente in questo gruppo.")

        # Aggiunge l'assenza del ragazzo al gruppo
        ragazzo.assenze.append(Assente(
            ragazzo_id=ragazzo.id,
            gruppo_id=gruppo.id
        ))
        db.commit()
        db.refresh(ragazzo)


def modifica_ragazzo_non_arrivato(ragazzo_id: int, group_id: int):
    with get_db_context() as db:
        ragazzo = db.query(Ragazzo).filter(Ragazzo.id == ragazzo_id).first()
        if not ragazzo:
            raise RagazzoNotFoundError(f"Ragazzo con ID {ragazzo_id} non trovato.")

        gruppo = db.query(Gruppo).filter(Gruppo.id == group_id).first()
        if not gruppo:
            raise GruppoNotFoundError(f"Gruppo con ID {group_id} non trovato.")

        # Controlla se il ragazzo è iscritto al gruppo
        iscrizioni = db.query(Iscrizione).filter(Iscrizione.gruppo_id == gruppo.id).all()
        if not any(ragazzo.id == r.id for iscrizione in iscrizioni for r in iscrizione.ragazzi):
            raise RagazzoNotFoundError(f"Ragazzo con ID {ragazzo_id} non iscritto a questo gruppo.")

        # Rimuove eventuali presenze o assenze precedenti del ragazzo nel gruppo
        for p in ragazzo.presenze:
            if p.gruppo_id == gruppo.id:
                db.delete(p)
                break

        for a in ragazzo.assenze:
            if a.gruppo_id == gruppo.id:
                db.delete(a)
                break

        # Aggiunge il ragazzo come non arrivato
        ragazzo.non_arrivato = True
        db.commit()
        db.refresh(ragazzo)


def modifica_fascia_oraria_orario_partenza(fascia_oraria_id: int, orario_partenza: int):
    with get_db_context() as db:
        fascia_oraria = db.query(FasciaOraria).filter(FasciaOraria.id == fascia_oraria_id).first()

        # Controlla se la fascia oraria esiste
        if not fascia_oraria:
            raise FasciaOrariaNotFoundError(f"Fascia oraria con ID {fascia_oraria_id} non trovata.")

        # Controlla se l'orario di partenza è valido
        try:
            orario_partenza = orario_partenza.strip()
            if not orario_partenza:
                raise ValueError("Orario di partenza non può essere vuoto")
        except ValueError as e:
            raise ValueError(str(e))

        # Aggiorna l'orario di partenza della fascia oraria
        fascia_oraria.oraInizio = orario_partenza
        db.commit()
        db.refresh(fascia_oraria)
        return fascia_oraria


def modifica_gruppo_nome(group_id: int, new_name: str):
    with get_db_context() as db:
        gruppo = db.query(Gruppo).filter(Gruppo.id == group_id).first()

        # Controlla se il gruppo esiste
        if not gruppo:
            raise GruppoNotFoundError(f"Gruppo con ID {group_id} non trovato.")

        # Controlla se il nuovo nome è valido
        if not new_name:
            raise InvalidGroupNameError("Il nome del gruppo non può essere vuoto.")

        # Aggiorna il nome del gruppo
        gruppo.nome = new_name
        db.commit()
        db.refresh(gruppo)
        return gruppo


def modifica_gruppo_tappa(group_id: int, numero_tappa: int, arrivato: bool):
    with get_db_context() as db:
        gruppo = db.query(Gruppo).join(Gruppo.fasciaOraria).join(FasciaOraria.percorso).join(Percorso.tappe).filter(
            Gruppo.id == group_id).first()

        # Controlla se il gruppo esiste
        if not gruppo:
            raise GruppoNotFoundError(f"Gruppo con ID {group_id} non trovato.")

        numero_tappa = int(numero_tappa)

        # Controlla se il numero di tappa è valido
        if numero_tappa < 0 or numero_tappa > len(gruppo.fasciaOraria.percorso.tappe):
            raise InvalidTappaNumberError("Il numero di tappa non può essere negativo.")

        # Aggiorna il numero della tappa e lo stato di arrivo del gruppo
        gruppo.numero_tappa = numero_tappa
        gruppo.arrivato = arrivato
        db.commit()
        db.refresh(gruppo)
        return gruppo


def crea_ragazzo_gruppo(group_id: int, name: str, surname: str, scuolaDiProvenienza_id: int = None,
                        genitore_id: int = None):
    with get_db_context() as db:
        gruppo = db.query(Gruppo).filter(Gruppo.id == group_id).first()

        if not gruppo:
            raise GruppoNotFoundError(f"Gruppo con ID {group_id} non trovato.")

        if not name or not surname:
            raise InvalidRagazzoDataError("Nome e cognome sono obbligatori.")

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

        return ragazzo, iscrizione

