from app.database import get_db
from app.models import Gruppo, FasciaOraria, Aula, Tappa, Percorso
from app.schemas.admin.dashboard.aula import AulaList, AulaResponse


def get_all_aule():
    """
    Legge tutte le aule dal database
    """
    db = next(get_db())

    aule = db.query(Aula).all()
    auleList = AulaList(aule=[])
    for aula in aule:
        occupata = False
        gruppoInAula = None
        tappa = db.query(Tappa).filter(Tappa.aula_id == aula.id).first()
        if tappa:
            percorsi = db.query(Percorso).filter(Percorso.id == tappa.percorso_id).all()
            for percorso in percorsi:
                gruppi = db.query(Gruppo).join(Gruppo.fasciaOraria).filter(
                    FasciaOraria.percorso_id == percorso.id).all()
                for gruppo in gruppi:
                    tappe = db.query(Tappa).order_by(Tappa.minuti_partenza).filter(
                        Tappa.percorso_id == percorso.id).all()
                    if (tappe[
                        gruppo.numero_tappa - 1].aula_id == aula.id
                            and gruppo.arrivato is True
                            and not gruppo.numero_tappa == 0):
                        occupata = True
                        gruppoInAula = gruppo
                        break
        if gruppoInAula is None:
            auleList.aule.append(AulaResponse(
                id=aula.id,
                nome=aula.nome,
                posizione=aula.posizione,
                materia=aula.materia,
                dettagli=aula.dettagli,
                occupata=occupata,
                minuti_arrivo=tappa.minuti_arrivo if tappa else None,
                minuti_partenza=tappa.minuti_partenza if tappa else None

            ))
            continue
        else:
            auleList.aule.append(AulaResponse(
                id=aula.id,
                nome=aula.nome,
                posizione=aula.posizione,
                materia=aula.materia,
                dettagli=aula.dettagli,
                occupata=occupata,
                gruppo_id=gruppoInAula.id,
                gruppo_nome=gruppoInAula.nome,
                gruppo_orario_partenza=gruppoInAula.fasciaOraria.oraInizio,
                minuti_arrivo=tappa.minuti_arrivo if tappa else None,
                minuti_partenza=tappa.minuti_partenza if tappa else None
            ))
    auleList.aule = sorted(auleList.aule,
                           key=lambda aula: aula.minuti_arrivo if aula.minuti_arrivo is not None else float('inf'))
    return auleList
