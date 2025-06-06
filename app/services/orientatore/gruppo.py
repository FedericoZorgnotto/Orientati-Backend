from app.database import get_db
from app.models import Gruppo, Percorso, Iscrizione, Presente, Assente, FasciaOraria
from app.schemas.orientatore.aula import AulaResponse
from app.schemas.orientatore.gruppo import GruppoResponse, GruppoResponsePresenze
from app.models.utente import Utente
from app.schemas.orientatore.tappa import TappaResponse


def get_gruppo_utente(current_user_id):
    db = next(get_db())
    current_user: Utente = db.query(Utente).filter(Utente.id == current_user_id).first()
    if current_user.gruppo_id is None:
        raise Exception("Utente non connesso a nessun gruppo")
    return current_user.gruppo_id


def get_gruppo(gruppo_id):
    """
    restituisce il gruppo al quale l'utente è connesso
    """
    db = next(get_db())

    gruppo: GruppoResponse = db.query(Gruppo).join(Gruppo.fasciaOraria).join(FasciaOraria.percorso).join(
        Percorso.tappe).filter(
        Gruppo.id == gruppo_id).first()
    if not gruppo:
        raise Exception("Gruppo non trovato")
    if not gruppo.fasciaOraria:
        raise Exception("Gruppo non associato a nessuna fascia oraria")
    if not gruppo.fasciaOraria.percorso:
        raise Exception("Gruppo non associato a nessun percorso")
    if not gruppo.fasciaOraria.percorso.tappe:
        raise Exception("Gruppo non associato a nessuna tappa")

    gruppo_partito = False
    if gruppo.numero_tappa > 0:
        percorso_partito = True

    percorso_finito = False
    if gruppo.numero_tappa == 0 and gruppo.arrivato:
        percorso_finito = True

    iscrizioni = db.query(Iscrizione).filter(Iscrizione.gruppo_id == gruppo.id).all()
    ragazzi = [ragazzo for iscrizione in iscrizioni for ragazzo in iscrizione.ragazzi]

    presenti = db.query(Presente).filter(Presente.gruppo_id == gruppo.id).all()
    assenti = db.query(Assente).filter(Assente.gruppo_id == gruppo.id).all()

    gruppoPresenze: GruppoResponsePresenze = GruppoResponsePresenze(
        nome=gruppo.nome,
        orario_partenza=gruppo.fasciaOraria.oraInizio,
        gruppo_partito=gruppo_partito,
        percorso_finito=percorso_finito,
        orientati_presenti=len(presenti),
        orientati_assenti=len(assenti),
        orientati_totali=len(ragazzi),
        tappa=get_tappa_gruppo(gruppo.id),
        tappa_successiva=get_tappa_gruppo(gruppo.id, successiva=True),
    )

    return gruppoPresenze


def get_tappa_gruppo(gruppo_id, successiva=False):
    """
    restituisce la tappa del gruppo
    """
    db = next(get_db())

    gruppo: GruppoResponse = db.query(Gruppo).join(Gruppo.fasciaOraria).join(FasciaOraria.percorso).join(
        Percorso.tappe).filter(
        Gruppo.id == gruppo_id).first()
    if not gruppo:
        raise Exception("Gruppo non trovato")

    if not gruppo.fasciaOraria:
        raise Exception("Gruppo non associato a nessuna fascia oraria")
    if not gruppo.fasciaOraria.percorso:
        raise Exception("Gruppo non associato a nessun percorso")
    if not gruppo.fasciaOraria.percorso.tappe:
        raise Exception("Gruppo non associato a nessuna tappa")

    tappa = None
    if gruppo.numero_tappa is not None:
        if successiva:
            if gruppo.numero_tappa + 1 < len(gruppo.fasciaOraria.percorso.tappe):
                tappa = gruppo.fasciaOraria.percorso.tappe[gruppo.numero_tappa + 1]
            else:
                return None
        else:
            tappa = gruppo.fasciaOraria.percorso.tappe[gruppo.numero_tappa]
    if tappa is None:
        raise Exception("Tappa non trovata per il gruppo")

    return TappaResponse(
        minuti_partenza=tappa.minuti_partenza,
        minuti_arrivo=tappa.minuti_arrivo,
        aula=AulaResponse(
            nome=tappa.aula.nome,
            posizione=tappa.aula.posizione,
            materia=tappa.aula.materia,
            dettagli=tappa.aula.dettagli,
        )
    )


def imposta_tappa_gruppo(gruppo_id, numero_tappa, arrivato):
    """
    imposta la tappa del gruppo
    """
    pass
