from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.middlewares.auth_middleware import admin_access
from app.models.tappa import Tappa
from app.schemas.tappa import TappaList, TappaCreate, TappaUpdate, TappaResponse

tappe_router = APIRouter()


@tappe_router.get("/", response_model=TappaList)
async def get_all_tappe(db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Legge tutte le tappe dal database
    """

    TappaList.aule = (db.query(Tappa).all())
    return TappaList


@tappe_router.get("/{tappa_id}", response_model=TappaResponse)
async def get_tappa(tappa_id: int, db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Legge una tappa dal database
    """
    if not (db.query(Tappa).filter(Tappa.id == tappa_id).first()):
        raise HTTPException(status_code=404, detail="Tappa not found")
    try:
        tappa = db.query(Tappa).filter(Tappa.id == tappa_id).first()
        return tappa
    except Exception as e:  # noqa: F841
        raise HTTPException(status_code=500, detail="Internal server error")


@tappe_router.put("/{tappa_id}", response_model=TappaResponse)
async def update_tappa(tappa_id: int, tappa_update: TappaUpdate, db: Session = Depends(get_db),
                       _=Depends(admin_access)):
    """
    Aggiorna una tappa nel database
    """

    db_tappa = db.query(Tappa).filter(Tappa.id == tappa_id).first()

    if not db_tappa:
        raise HTTPException(status_code=404, detail="Tappa not found")

    if tappa_update.percorso_id is not None:
        db_tappa.percorso_id = tappa_update.percorso_id
    if tappa_update.aula_id is not None:
        db_tappa.aula_id = tappa_update.aula_id
    if tappa_update.minuti_arrivo is not None:
        db_tappa.minuti_arrivo = tappa_update.minuti_arrivo
    if tappa_update.minuti_partenza is not None:
        db_tappa.minuti_partenza = tappa_update.minuti_part

    db.commit()
    db.refresh(db_tappa)

    return db_tappa


@tappe_router.post("/", response_model=TappaResponse)
async def create_tappa(tappa: TappaCreate, db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Crea una tappa nel database
    """

    db_tappa = Tappa(
        percorso_id=tappa.percorso_id,
        aula_id=tappa.aula_id,
        minuti_arrivo=tappa.minuti_arrivo,
        minuti_partenza=tappa.minuti_partenza
    )

    db.add(db_tappa)
    db.commit()
    db.refresh(db_tappa)
    return db_tappa


@tappe_router.delete("/{tappa_id}")
async def delete_tappa(tappa_id: int, db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Cancella una tappa dal database
    """
    if not db.query(Tappa).filter(Tappa.id == tappa_id).first():
        raise HTTPException(status_code=404, detail="Tappa not found")
    try:
        db.query(Tappa).filter(Tappa.id == tappa_id).delete()
        db.commit()
        return {"message": "Tappa deleted successfully"}
    except Exception as e:
        if e.args[0] == 1451:
            raise HTTPException(status_code=400, detail="Tappa has dependencies")
        else:
            raise HTTPException(status_code=500, detail="Internal server error")
