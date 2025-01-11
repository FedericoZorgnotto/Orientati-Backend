from app.database import get_db
from app.models import Gruppo


def crea_codice_gruppo():
    """
    Funzione che crea un codice univoco per il gruppo
    """

    db = next(get_db())
    try:
        # crea un codice univoco che non esiste già nel database
        codice = None
        while True:
            codice = Gruppo.genera_codice()
            if not db.query(Gruppo).filter(Gruppo.codice == codice).first():
                break
        return codice

    except Exception as e:
        print(f"Errore durante la creazione del codice gruppo: {e}")
    finally:
        db.close()
