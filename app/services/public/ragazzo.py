from app.database import get_db
from app.models import Ragazzo, Indirizzo


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

    if ragazzo.indirizziDiInteresse:
        for indirizzo_id in ragazzo.indirizziDiInteresse:
            indirizzo = database.query(Indirizzo).filter(Indirizzo.id == indirizzo_id).first()
            if indirizzo:
                ragazzo_db.indirizziDiInteresse.append(indirizzo)

        database.commit()
        database.refresh(ragazzo_db)

    return ragazzo_db


def ragazzo_from_ragazzo_id(ragazzo_id):
    """
    Restituisce un ragazzo associato a un genitore
    """
    database = next(get_db())
    ragazzo = database.query(Ragazzo).filter(Ragazzo.id == ragazzo_id).first()
    if not ragazzo:
        return None
    return ragazzo


def delete_ragazzo_from_ragazzo_id(ragazzo_id):
    """
    Elimina un ragazzo associato a un genitore
    """
    database = next(get_db())
    ragazzo = database.query(Ragazzo).filter(Ragazzo.id == ragazzo_id).first()
    if not ragazzo:
        return None
    database.delete(ragazzo)
    database.commit()
    return ragazzo


def edit_ragazzo(ragazzo, ragazzo_data):
    database = next(get_db())
    ragazzo.nome = ragazzo_data.nome
    ragazzo.cognome = ragazzo_data.cognome
    ragazzo.scuolaDiProvenienza_id = ragazzo_data.scuolaDiProvenienza_id

    # aggiorna gli indirizzi di interesse
    ragazzo.indirizziDiInteresse.clear()
    if ragazzo_data.indirizziDiInteresse:
        for indirizzo_id in ragazzo_data.indirizziDiInteresse:
            indirizzo = database.query(Indirizzo).filter(Indirizzo.id == indirizzo_id).first()
            if indirizzo:
                ragazzo.indirizziDiInteresse.append(indirizzo)

    database.commit()
    database.refresh(ragazzo)
    return ragazzo
