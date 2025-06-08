from datetime import datetime

from app.database import get_db
from app.models import Gruppo, Iscrizione, Presente, Assente, FasciaOraria, Data
from app.schemas.admin.dashboard.orientato import OrientatoList, OrientatoBase, IscrizioneList, IscrizioneBase


def get_all_orientati(percorso_id: str | int):
    """
    Legge tutti gli orientati del giorno dal database
    """
    db = next(get_db())
    percorso_id = int(percorso_id)

    gruppi = db.query(Gruppo).join(Gruppo.fasciaOraria).join(FasciaOraria.data).filter(
        Data.data == datetime.now().strftime("%Y-%m-%d"),
        FasciaOraria.percorso_id == percorso_id
    ).all()
    # ordino i gruppi per fascia oraria
    gruppi = sorted(gruppi, key=lambda gruppo: gruppo.fasciaOraria.oraInizio)

    lista_iscrizoni = IscrizioneList(iscrizioni=[])

    for gruppo in gruppi:
        db_gruppo = db.query(Gruppo).filter(Gruppo.id == gruppo.id).first()
        iscrizioni = db.query(Iscrizione).join(Iscrizione.fasciaOraria).filter(Iscrizione.gruppo_id == gruppo.id).all()

        presenti = db.query(Presente).filter(Presente.gruppo_id == gruppo.id).all()
        assenti = db.query(Assente).filter(Assente.gruppo_id == gruppo.id).all()

        for iscrizione in iscrizioni:
            if not any(iscrizione.ragazzi):
                continue
            ragazzi = iscrizione.ragazzi
            orientati = OrientatoList(orientati=[])

            for ragazzo in ragazzi:
                orientato = OrientatoBase(
                    id=ragazzo.id,
                    nome=ragazzo.nome,
                    cognome=ragazzo.cognome,
                    scuolaDiProvenienza_id=ragazzo.scuolaDiProvenienza_id,
                    scuolaDiProvenienza_nome=ragazzo.scuolaDiProvenienza.nome,
                    gruppo_id=db_gruppo.id,
                    gruppo_nome=db_gruppo.nome,
                    gruppo_orario_partenza=db_gruppo.fasciaOraria.oraInizio
                )
                if ragazzo.id in [presente.ragazzo_id for presente in presenti]:
                    orientato.presente = True
                else:
                    orientato.presente = False
                if ragazzo.id in [assente.ragazzo_id for assente in assenti]:
                    orientato.assente = True
                else:
                    orientato.assente = False
                orientati.orientati.append(orientato)
            lista_iscrizoni.iscrizioni.append(
                IscrizioneBase(
                    genitore_id=iscrizione.genitore_id,
                    fascia_oraria_id=iscrizione.fasciaOraria_id,
                    gruppo_id=iscrizione.gruppo_id,
                    orientati=orientati.orientati
                )
            )
    return lista_iscrizoni
