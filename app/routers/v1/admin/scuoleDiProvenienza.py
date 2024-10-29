from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.middlewares.auth_middleware import admin_access
from app.models.scuolaDiProvenienza import ScuolaDiProvenienza
from app.schemas.ScuolaDiProvenienza import ScuolaDiProvenienzaList, ScuolaDiProvenienzaBaseAdmin, \
    ScuolaDiProvenienzaCreate, ScuolaDiProvenienzaUpdate

scuoleDiProvenienza_router = APIRouter()


@scuoleDiProvenienza_router.get("/", response_model=ScuolaDiProvenienzaList)
async def get_all_scuoleDiProvenienza(db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Legge tutte le scuole di provenienza dal database
    """

    ScuolaDiProvenienzaList.scuoleDiProvenienza = db.query(ScuolaDiProvenienza).all()
    return ScuolaDiProvenienzaList


@scuoleDiProvenienza_router.get("/{scuolaDiProvenienza_id}", response_model=ScuolaDiProvenienzaBaseAdmin)
async def get_scuolaDiProvenienza(scuolaDiProvenienza_id: int, db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Legge una scuola di provenienza dal database
    """
    if not db.query(ScuolaDiProvenienza).filter(ScuolaDiProvenienza.id == scuolaDiProvenienza_id).first():
        raise HTTPException(status_code=404, detail="ScuolaDiProvenienza not found")
    try:
        scuolaDiProvenienza = db.query(ScuolaDiProvenienza).filter(
            ScuolaDiProvenienza.id == scuolaDiProvenienza_id).first()
        return scuolaDiProvenienza
    except Exception as e:  # noqa: F841
        raise HTTPException(status_code=500, detail="Internal server error")


@scuoleDiProvenienza_router.post("/", response_model=ScuolaDiProvenienzaBaseAdmin)
async def create_scuolaDiProvenienza(scuolaDiProvenienza: ScuolaDiProvenienzaCreate, db: Session = Depends(get_db),
                                     _=Depends(admin_access)):
    """
    Crea una scuola di provenienza nel database
    """

    db_scuolaDiProvenienza = ScuolaDiProvenienza(
        nome=scuolaDiProvenienza.nome,
        citta=scuolaDiProvenienza.citta
    )

    db.add(db_scuolaDiProvenienza)
    db.commit()
    db.refresh(db_scuolaDiProvenienza)
    return db_scuolaDiProvenienza


@scuoleDiProvenienza_router.put("/{scuolaDiProvenienza_id}", response_model=ScuolaDiProvenienzaBaseAdmin)
async def update_scuolaDiProvenienza(scuolaDiProvenienza_id: int, scuolaDiProvenienza_update: ScuolaDiProvenienzaUpdate,
                                     db: Session = Depends(get_db),
                                     _=Depends(admin_access)):
    """
    Aggiorna una scuola di provenienza nel database
    """
    db_scuolaDiProvenienza = db.query(ScuolaDiProvenienza).filter(
        ScuolaDiProvenienza.id == scuolaDiProvenienza_id).first()

    if not db_scuolaDiProvenienza:
        raise HTTPException(status_code=404, detail="ScuolaDiProvenienza not found")

    if scuolaDiProvenienza_update.nome is not None:
        db_scuolaDiProvenienza.nome = scuolaDiProvenienza_update.nome
    if scuolaDiProvenienza_update.citta is not None:
        db_scuolaDiProvenienza.citta = scuolaDiProvenienza_update.citta

    db.commit()
    db.refresh(db_scuolaDiProvenienza)

    return db_scuolaDiProvenienza


@scuoleDiProvenienza_router.delete("/{scuolaDiProvenienza_id}")
async def delete_scuolaDiProvenienza(scuolaDiProvenienza_id: int, db: Session = Depends(get_db),
                                     _=Depends(admin_access)):
    """
    Cancella unascuola di provenienza dal database
    """
    if not db.query(ScuolaDiProvenienza).filter(ScuolaDiProvenienza.id == scuolaDiProvenienza_id).first():
        raise HTTPException(status_code=404, detail="ScuolaDiProvenienza not found")
    try:
        db.query(ScuolaDiProvenienza).filter(ScuolaDiProvenienza.id == scuolaDiProvenienza_id).delete()
        db.commit()
        return {"message": "ScuolaDiProvenienza deleted successfully"}
    except Exception as e:
        if e.args[0] == 1451:
            raise HTTPException(status_code=400, detail="ScuolaDiProvenienza has dependencies")
        else:
            raise HTTPException(status_code=500, detail="Internal server error")
