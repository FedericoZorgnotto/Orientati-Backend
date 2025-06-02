from app.database import get_db
from app.models import Gruppo, Percorso, Iscrizione, Presente, Assente, FasciaOraria
from app.schemas.orientatore.gruppo import GruppoResponse, GruppoResponsePresenze
from app.models.utente import Utente


def get_gruppo_utente(current_user_id):
    """
    restituisce il gruppo al quale l'utente è connesso
    """
    db = next(get_db())
    current_user: Utente = db.query(Utente).filter(Utente.id == current_user_id).first()
    if current_user.gruppo_id is None:
        raise Exception("Utente non connesso a nessun gruppo")

    gruppo: GruppoResponse = db.query(Gruppo).join(Gruppo.fasciaOraria).join(FasciaOraria.percorso).join(
        Percorso.tappe).filter(
        Gruppo.id == current_user.gruppo_id).first()
    if not gruppo:
        raise Exception("Gruppo non trovato")
    if not gruppo.fasciaOraria:
        raise Exception("Gruppo non associato a nessuna fascia oraria")
    if not gruppo.fasciaOraria.percorso:
        raise Exception("Gruppo non associato a nessun percorso")
    if not gruppo.fasciaOraria.percorso.tappe:
        raise Exception("Gruppo non associato a nessuna tappa")

    percorso_finito = False
    if gruppo.numero_tappa == 0 and gruppo.arrivato:
        percorso_finito = True
    gruppoPresenze: GruppoResponsePresenze = GruppoResponsePresenze(
        id=gruppo.id,
        nome=gruppo.nome,
        orario_partenza=gruppo.fasciaOraria.oraInizio,
        percorso_id=gruppo.fasciaOraria.percorso_id,
        numero_tappa=gruppo.numero_tappa,
        arrivato=gruppo.arrivato,
        percorso_finito=percorso_finito
    )

    iscrizioni = db.query(Iscrizione).filter(Iscrizione.gruppo_id == gruppo.id).all()
    ragazzi = [ragazzo for iscrizione in iscrizioni for ragazzo in iscrizione.ragazzi]

    presenti = db.query(Presente).filter(Presente.gruppo_id == gruppo.id).all()
    assenti = db.query(Assente).filter(Assente.gruppo_id == gruppo.id).all()

    gruppoPresenze.orientati_presenti = len(presenti)
    gruppoPresenze.orientati_assenti = len(assenti)
    gruppoPresenze.orientati_totali = len(ragazzi)

    return gruppoPresenze


def get_tappe_gruppo(gruppi_id):
    """
    restituisce le tappe del gruppo
    """
    pass


def get_tappa_gruppo(gruppo_id, numero_tappa):
    """
    restituisce la tappa N del gruppo
    """
    pass


def imposta_tappa_gruppo(gruppo_id, numero_tappa, arrivato):
    """
    imposta la tappa del gruppo
    """
    pass
