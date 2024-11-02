from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.middlewares.auth_middleware import admin_access
from app.models.aula import Aula
from app.schemas.aula import AulaList, AulaCreate, AulaUpdate, AulaResponse

aule_router = APIRouter()


@aule_router.get("/", response_model=AulaList)
async def get_all_aule(db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Legge tutte le aule dal database
    """

    AulaList.aule = (db.query(Aula).all())
    return AulaList


@aule_router.get("/{aula_id}", response_model=AulaResponse)
async def get_aula(aula_id: int, db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Legge un'aula dal database
    """
    if not (db.query(Aula).filter(Aula.id == aula_id).first()):
        raise HTTPException(status_code=404, detail="Aula not found")
    try:
        aula = db.query(Aula).filter(Aula.id == aula_id).first()
        return aula
    except Exception as e:  # noqa: F841
        raise HTTPException(status_code=500, detail="Internal server error")


@aule_router.put("/{aula_id}", response_model=AulaResponse)
async def update_aula(aula_id: int, aula_update: AulaUpdate, db: Session = Depends(get_db),
                      _=Depends(admin_access)):
    """
    Aggiorna un'aula nel database
    """

    db_aula = db.query(Aula).filter(Aula.id == aula_id).first()

    if not db_aula:
        raise HTTPException(status_code=404, detail="Aula not found")

    if aula_update.nome is not None:
        db_aula.nome = aula_update.nome
    if aula_update.posizione is not None:
        db_aula.posizione = aula_update.posizione
    if aula_update.materia is not None:
        db_aula.materia = aula_update.materia
    if aula_update.dettagli is not None:
        db_aula.dettagli = aula_update.dettagli

    db.commit()
    db.refresh(db_aula)

    return db_aula


@aule_router.post("/", response_model=AulaResponse)
async def create_aula(aula: AulaCreate, db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Crea un'aula nel database
    """

    db_aula = Aula(
        nome=aula.nome,
        posizione=aula.posizione,
        materia=aula.materia,
        dettagli=aula.dettagli
    )

    db.add(db_aula)
    db.commit()
    db.refresh(db_aula)
    return db_aula


@aule_router.delete("/{aula_id}")
async def delete_aula(aula_id: int, db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Cancella un'aula dal database
    """
    if not db.query(Aula).filter(Aula.id == aula_id).first():
        raise HTTPException(status_code=404, detail="Aula not found")
    try:
        db.query(Aula).filter(Aula.id == aula_id).delete()
        db.commit()
        return {"message": "Aula deleted successfully"}
    except Exception as e:
        if e.args[0] == 1451:
            raise HTTPException(status_code=400, detail="Aula has dependencies")
        else:
            raise HTTPException(status_code=500, detail="Internal server error")
