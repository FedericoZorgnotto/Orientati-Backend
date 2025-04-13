from collections import defaultdict

from sqlalchemy.orm import joinedload

from app.database import get_db
from app.models.data import Data
from app.models.fasciaOraria import FasciaOraria
from app.schemas.date import PercorsoConFasce, FasciaOrariaBase, Data as DataSchema


def get_all_date():
    """
    Restituisce tutte le date con opzione per includere le fasce orarie
    :return: Lista di oggetti Data
    """
    database = next(get_db())
    date_raw = database.query(Data).options(
        joinedload(Data.fasceOrarie).joinedload(FasciaOraria.percorso)
    ).all()
    date = organize_by_percorso(date_raw)
    return date


def organize_by_percorso(date_list):
    """
    Riorganizza i dati raggruppando le fasce orarie per percorso
    """
    result = []

    for data in date_list:
        # Crea un dizionario per raggruppare le fasce orarie per percorso
        percorsi_dict = defaultdict(list)

        for fascia in data.fasceOrarie:
            # Crea un oggetto FasciaOrariaBase senza il percorso_id
            fascia_base = FasciaOrariaBase(
                id=fascia.id,
                oraInizio=fascia.oraInizio
            )

            # Aggiungi la fascia al percorso corrispondente
            percorsi_dict[fascia.percorso.id].append(fascia_base)

        # Crea la lista di percorsi con le fasce orarie associate
        percorsi_list = []
        for percorso_id, fasce in percorsi_dict.items():
            # Trova il nome del percorso
            nome_percorso = next((fascia.percorso.nome for fascia in data.fasceOrarie
                                  if fascia.percorso.id == percorso_id), "")

            percorso = PercorsoConFasce(
                id=percorso_id,
                nome=nome_percorso,
                fasce=fasce
            )
            percorsi_list.append(percorso)

        # Crea l'oggetto Data con i percorsi associati
        data_obj = DataSchema(
            id=data.id,
            data=data.data,
            percorsi=percorsi_list
        )

        result.append(data_obj)

    return result
