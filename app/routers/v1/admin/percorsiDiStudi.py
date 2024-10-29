from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.middlewares.auth_middleware import admin_access
from app.models.percorsoDiStudi import PercorsoDiStudi
from app.schemas.percorsoDiStudi import (PercorsoDiStudiList, PercorsoDiStudiBaseAdmin, PercorsoDiStudiCreate,
                                         PercorsoDiStudiUpdate)

percorsiDiStudi_router = APIRouter()


@percorsiDiStudi_router.get("/", response_model=PercorsoDiStudiList)
async def get_all_percorsiDiStudi(db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Legge tutti i percorsi di studi dal database
    """

    PercorsoDiStudiList.percorsiDiStudi = db.query(PercorsoDiStudi).all()
    return PercorsoDiStudiList


@percorsiDiStudi_router.get("/{percorsoDiStudi_id}", response_model=PercorsoDiStudiBaseAdmin)
async def get_percorsoDiStudi(percorsoDiStudi_id: int, db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Legge un percorso di studi dal database
    """
    if not db.query(PercorsoDiStudi).filter(PercorsoDiStudi.id == percorsoDiStudi_id).first():
        raise HTTPException(status_code=404, detail="PercorsoDiStudi not found")
    try:
        percorsoDiStudi = db.query(PercorsoDiStudi).filter(PercorsoDiStudi.id == percorsoDiStudi_id).first()
        return percorsoDiStudi
    except Exception as e:  # noqa: F841
        raise HTTPException(status_code=500, detail="Internal server error")


@percorsiDiStudi_router.post("/", response_model=PercorsoDiStudiBaseAdmin)
async def create_percorsoDiStudi(percorsoDiStudi: PercorsoDiStudiCreate, db: Session = Depends(get_db),
                                 _=Depends(admin_access)):
    """
    Crea un percorso di studi nel database
    """

    db_percorsoDiStudi = PercorsoDiStudi(
        nome=percorsoDiStudi.nome
    )

    db.add(db_percorsoDiStudi)
    db.commit()
    db.refresh(db_percorsoDiStudi)
    return db_percorsoDiStudi


@percorsiDiStudi_router.put("/{percorsoDiStudi_id}", response_model=PercorsoDiStudiBaseAdmin)
async def update_percorsoDiStudi(percorsoDiStudi_id: int, percorsoDiStudi_update: PercorsoDiStudiUpdate,
                                 db: Session = Depends(get_db),
                                 _=Depends(admin_access)):
    """
    Aggiorna un percorso di studi nel database
    """
    db_percorsoDiStudi = db.query(PercorsoDiStudi).filter(PercorsoDiStudi.id == percorsoDiStudi_id).first()

    if not db_percorsoDiStudi:
        raise HTTPException(status_code=404, detail="PercorsoDiStudi not found")

    if percorsoDiStudi_update.nome is not None:
        db_percorsoDiStudi.nome = percorsoDiStudi_update.nome

    db.commit()
    db.refresh(db_percorsoDiStudi)

    return db_percorsoDiStudi


@percorsiDiStudi_router.delete("/{percorsoDiStudi_id}")
async def delete_percorsoDiStudi(percorsoDiStudi_id: int, db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Cancella un percorso di studi dal database
    """
    if not db.query(PercorsoDiStudi).filter(PercorsoDiStudi.id == percorsoDiStudi_id).first():
        raise HTTPException(status_code=404, detail="PercorsoDiStudi not found")
    try:
        db.query(PercorsoDiStudi).filter(PercorsoDiStudi.id == percorsoDiStudi_id).delete()
        db.commit()
        return {"message": "PercorsoDiStudi deleted successfully"}
    except Exception as e:
        if e.args[0] == 1451:
            raise HTTPException(status_code=400, detail="PercorsoDiStudi has dependencies")
        else:
            raise HTTPException(status_code=500, detail="Internal server error")
