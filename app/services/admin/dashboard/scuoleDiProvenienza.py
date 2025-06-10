from app.database import get_db_context
from app.models import ScuolaDiProvenienza


def get_all_scuole():
    with get_db_context() as db:
        scuole = db.query(ScuolaDiProvenienza).all()
        return scuole
