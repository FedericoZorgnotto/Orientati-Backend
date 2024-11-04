from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.middlewares.auth_middleware import admin_access
from app.models.percorso import Percorso
from app.schemas.percorso import PercorsoList, PercorsoResponse, PercorsoUpdate, PercorsoCreate

percorsi_router = APIRouter()


@percorsi_router.get("/", response_model=PercorsoList)
async def get_all_percorsi(db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Legge tutti i percorsi dal database
    """

    PercorsoList.percorsi = (db.query(Percorso).all())
    return PercorsoList


@percorsi_router.get("/{percorso_id}", response_model=PercorsoResponse)
async def get_percorso(percorso_id: int, db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Legge un percorso dal database
    """
    if not (db.query(Percorso).filter(Percorso.id == percorso_id).first()):
        raise HTTPException(status_code=404, detail="Percorso not found")
    try:
        percorso = db.query(Percorso).filter(Percorso.id == percorso_id).first()
        return percorso
    except Exception as e:  # noqa: F841
        raise HTTPException(status_code=500, detail="Internal server error")


@percorsi_router.put("/{percorso_id}", response_model=PercorsoResponse)
async def update_percorso(percorso_id: int, percorso_update: PercorsoUpdate, db: Session = Depends(get_db),
                          _=Depends(admin_access)):
    """
    Aggiorna un percorso nel database
    """

    db_percorso = db.query(Percorso).filter(Percorso.id == percorso_id).first()

    if not db_percorso:
        raise HTTPException(status_code=404, detail="Percorso not found")

    if percorso_update.nome is not None:
        db_percorso.nome = percorso_update.nome
    if percorso_update.percorsoDiStudi_id is not None:
        db_percorso.percorsoDiStudi_id = percorso_update.percorsoDiStudi_id

    db.commit()
    db.refresh(db_percorso)

    return db_percorso


@percorsi_router.post("/", response_model=PercorsoResponse)
async def create_percorso(percorso: PercorsoCreate, db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Crea un percorso nel database
    """

    db_percorso = Percorso(
        nome=percorso.nome,
        percorsoDiStudi_id=percorso.percorsoDiStudi_id
    )

    db.add(db_percorso)
    db.commit()
    db.refresh(db_percorso)
    return db_percorso


@percorsi_router.delete("/{percorso_id}")
async def delete_percorso(percorso_id: int, db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Cancella un percorso dal database
    """
    if not db.query(Percorso).filter(Percorso.id == percorso_id).first():
        raise HTTPException(status_code=404, detail="Percorso not found")
    try:
        db.query(Percorso).filter(Percorso.id == percorso_id).delete()
        db.commit()
        return {"message": "Percorso deleted successfully"}
    except Exception as e:
        if e.args[0] == 1451:
            raise HTTPException(status_code=400, detail="Percorso has dependencies")
        else:
            raise HTTPException(status_code=500, detail="Internal server error")
