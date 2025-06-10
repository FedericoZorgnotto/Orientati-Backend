from app.database import get_db_context
from app.models import Ragazzo


def get_all_ragazzi():
    with get_db_context() as db:
        ragazzi = db.query(Ragazzo).distinct().all()
        ragazzi_list = [{
            "id": ragazzo.id,
            "nome": ragazzo.nome,
            "cognome": ragazzo.cognome,
            "scuolaDiProvenienza_id": ragazzo.scuolaDiProvenienza_id if ragazzo.scuolaDiProvenienza else None,
            "genitore_id": ragazzo.genitore_id if ragazzo.genitore else None,
        } for ragazzo in ragazzi if ragazzo is not None]
        return ragazzi_list
