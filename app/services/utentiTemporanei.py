from app.database import get_db
from app.models import Utente


def elimina_utenti_temporanei():
    """
    Funzione che elimina gli utenti temporanei scaduti.
    """

    db = get_db()
    try:
        utenti_temporanei = db.query(Utente).filter(Utente.temporaneo == True).all()  # noqa E712
        for user in utenti_temporanei:
            db.delete(user)
        db.commit()
    except Exception as e:
        print(f"Errore durante la cancellazione degli utenti: {e}")
        db.rollback()
    finally:
        db.close()
