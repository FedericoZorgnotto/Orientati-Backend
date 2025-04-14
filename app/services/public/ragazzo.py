from app.database import get_db
from app.models import Ragazzo


def ragazzi_from_genitore(genitore):
    """
    Restituisce i ragazzi associati a un genitore
    """
    ragazzi = []
    for ragazzo in genitore.ragazzi:
        ragazzi.append(ragazzo)
    return ragazzi


def add_ragazzo(ragazzo, genitore_id):
    """
    Aggiunge un ragazzo associato a un genitore
    """
    database = next(get_db())
    ragazzo_db = Ragazzo(
        nome=ragazzo.nome,
        cognome=ragazzo.cognome,
        genitore_id=genitore_id,
        scuolaDiProvenienza_id=ragazzo.scuolaDiProvenienza_id,
    )
    database.add(ragazzo_db)
    database.commit()
    database.refresh(ragazzo_db)
    return ragazzo_db
