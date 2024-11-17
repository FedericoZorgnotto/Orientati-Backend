from app.database import get_db
from app.models.logUtente import CategoriaLogUtente as CategoriaLogUtenteEnum, LogUtente


async def log_user_action(categoria: CategoriaLogUtenteEnum, azione: str, utente_id: int = None,
                          dati: {} = None):
    db = next(get_db())
    if dati:
        dati = {k: str(v) for k, v in dati.items()}
    db_log_entry = LogUtente(
        utente_id=utente_id,
        categoria=categoria,
        azione=azione,
        dati=dati.__str__()
    )
    db.add(db_log_entry)
    db.commit()
