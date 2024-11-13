from app.database import get_db
from app.models import Orientatore

def crea_codice_orientatore():
    """
    Funzione che crea un codice univoco per l'orientatore
    """

    db = next(get_db())
    try:
        # crea un codice univoco che non esiste già nel database
        codice = None
        while True:
            codice = Orientatore.genera_codice()
            if not db.query(Orientatore).filter(Orientatore.codice == codice).first():
                break
        return codice

    except Exception as e:
        print(f"Errore durante la creazione del codice orientatore: {e}")
    finally:
        db.close()