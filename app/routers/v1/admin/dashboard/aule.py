from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.middlewares.auth_middleware import admin_access
from app.models import Gruppo, Aula, Tappa, Percorso
from app.schemas.dashboard.aula import AulaList, AulaResponse

aule_router = APIRouter()


@aule_router.get("/", response_model=AulaList)
async def get_all_aule(db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Legge tutte le aule dal database
    """

    aule = db.query(Aula).all()
    auleList = AulaList(aule=[])
    for aula in aule:
        occupata = False
        gruppoInAula = None
        tappa = db.query(Tappa).filter(Tappa.aula_id == aula.id).first()
        if tappa:
            percorsi = db.query(Percorso).filter(Percorso.id == tappa.percorso_id).all()
            for percorso in percorsi:
                gruppi = db.query(Gruppo).filter(Gruppo.percorso_id == percorso.id).all()
                for gruppo in gruppi:
                    if percorso.tappe[
                        gruppo.numero_tappa - 1].aula_id == aula.id and gruppo.arrivato is True and not gruppo.numero_tappa == 0:
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
                gruppo_orario_partenza=gruppoInAula.orario_partenza,
                minuti_arrivo=tappa.minuti_arrivo if tappa else None,
                minuti_partenza=tappa.minuti_partenza if tappa else None
            ))

    return auleList
