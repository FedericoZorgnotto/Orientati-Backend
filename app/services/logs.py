from app.database import get_db
from app.models.logUtente import CategoriaLogUtente as CategoriaLogUtenteEnum, LogUtente


async def log_user_action(utente_id: int, categoria: CategoriaLogUtenteEnum, azione: str,
                          dati: str = None):
    db = next(get_db())
    db_log_entry = LogUtente(
        utente_id=utente_id,
        categoria=categoria,
        azione=azione,
        dati=dati)
    print(f"Log entry: {db_log_entry}")  # TODO: rimuovere
    db.add(db_log_entry)
    db.commit()
