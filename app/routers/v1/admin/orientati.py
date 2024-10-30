from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.middlewares.auth_middleware import admin_access
from app.models import ScuolaDiProvenienza
from app.models.orientato import Orientato
from app.schemas.orientato import OrientatoList, OrientatoBaseAdmin, OrientatoCreate, OrientatoUpdate, OrientatoResponse

orientati_router = APIRouter()


@orientati_router.get("/", response_model=OrientatoList)
async def get_all_orientati(db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Legge tutti gli orientati dal database
    """

    OrientatoList.orientati = db.query(Orientato).all()
    for orientato in OrientatoList.orientati:
        orientato.nomeScuolaDiProvenienza = orientato.scuolaDiProvenienza.nome
    return OrientatoList


@orientati_router.get("/{orientato_id}", response_model=OrientatoResponse)
async def get_orientato(orientato_id: int, db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Legge un'orientato dal database
    """
    if not db.query(Orientato).filter(Orientato.id == orientato_id).first():
        raise HTTPException(status_code=404, detail="Orientato not found")
    try:
        orientato = db.query(Orientato).filter(Orientato.id == orientato_id).first()
        orientato.nomeScuolaDiProvenienza = orientato.scuolaDiProvenienza.nome
        return orientato
    except Exception as e:  # noqa: F841
        raise HTTPException(status_code=500, detail="Internal server error")


@orientati_router.post("/", response_model=OrientatoResponse)
async def create_orientato(orientato: OrientatoCreate, db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Crea un'orientato nel database
    """

    if not db.query(ScuolaDiProvenienza).filter(ScuolaDiProvenienza.id == orientato.scuolaDiProvenienza_id).first():
        raise HTTPException(status_code=404, detail="ScuolaDiProvenienza not found")

    db_orientato = Orientato(
        nome=orientato.nome,
        cognome=orientato.cognome,
        scuolaDiProvenienza_id=orientato.scuolaDiProvenienza_id
    )

    db.add(db_orientato)
    db.commit()
    db.refresh(db_orientato)
    OrientatoResponse = db_orientato
    OrientatoResponse.nomeScuolaDiProvenienza = db_orientato.scuolaDiProvenienza.nome
    return OrientatoResponse


@orientati_router.put("/{orientato_id}", response_model=OrientatoBaseAdmin)
async def update_orientato(orientato_id: int, orientato_update: OrientatoUpdate, db: Session = Depends(get_db),
                           _=Depends(admin_access)):
    """
    Aggiorna un'orientato nel database
    """

    if not db.query(ScuolaDiProvenienza).filter(
            ScuolaDiProvenienza.id == orientato_update.scuolaDiProvenienza_id).first():
        raise HTTPException(status_code=404, detail="ScuolaDiProvenienza not found")

    db_orientato = db.query(Orientato).filter(Orientato.id == orientato_id).first()

    if not db_orientato:
        raise HTTPException(status_code=404, detail="Orientato not found")

    if orientato_update.nome is not None:
        db_orientato.nome = orientato_update.nome
    if orientato_update.cognome is not None:
        db_orientato.cognome = orientato_update.cognome
    if orientato_update.scuolaDiProvenienza_id is not None:
        db_orientato.scuolaDiProvenienza_id = orientato_update.scuolaDiProvenienza_id

    db.commit()
    db.refresh(db_orientato)

    return db_orientato


@orientati_router.delete("/{orientato_id}")
async def delete_orientato(orientato_id: int, db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Cancella un'orientato dal database
    """
    if not db.query(Orientato).filter(Orientato.id == orientato_id).first():
        raise HTTPException(status_code=404, detail="Orientato not found")
    try:
        db.query(Orientato).filter(Orientato.id == orientato_id).delete()
        db.commit()
        return {"message": "Orientato deleted successfully"}
    except Exception as e:
        if e.args[0] == 1451:
            raise HTTPException(status_code=400, detail="Orientato has dependencies")
        else:
            raise HTTPException(status_code=500, detail="Internal server error")
