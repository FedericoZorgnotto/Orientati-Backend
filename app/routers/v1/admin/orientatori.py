from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.middlewares.auth_middleware import admin_access
from app.models import Indirizzo
from app.models.orientatore import Orientatore
from app.schemas.orientatore import OrientatoreList, OrientatoreBaseAdmin, OrientatoreCreate, OrientatoreUpdate, \
    OrientatoreResponse
from app.services.orientatori import crea_codice_orientatore

orientatori_router = APIRouter()


@orientatori_router.get("/", response_model=OrientatoreList)
async def get_all_orientatori(db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Legge tutti gli orientatori dal database
    """

    OrientatoreList.orientatori = db.query(Orientatore).all()
    for orientatore in OrientatoreList.orientatori:
        orientatore.nomeIndirizzo = orientatore.indirizzo.nome
    return OrientatoreList


@orientatori_router.get("/{orientatore_id}", response_model=OrientatoreResponse)
async def get_orientatore(orientatore_id: int, db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Legge un'orientatore dal database
    """
    if not db.query(Orientatore).filter(Orientatore.id == orientatore_id).first():
        raise HTTPException(status_code=404, detail="Orientatore not found")
    try:
        orientatore = db.query(Orientatore).filter(Orientatore.id == orientatore_id).first()
        orientatore.nomeIndirizzo = orientatore.indirizzo.nome
        return orientatore
    except Exception as e:  # noqa: F841
        raise HTTPException(status_code=500, detail="Internal server error")


@orientatori_router.get("/rigeneraCodice/{orientatore_id}", response_model=OrientatoreResponse)
async def rigenera_codice_orientatore(orientatore_id: int, db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Rigenera il codice di un orientatore
    """
    if not db.query(Orientatore).filter(Orientatore.id == orientatore_id).first():
        raise HTTPException(status_code=404, detail="Orientatore not found")
    try:
        orientatore = db.query(Orientatore).filter(Orientatore.id == orientatore_id).first()
        orientatore.codice = crea_codice_orientatore()
        db.commit()
        db.refresh(orientatore)
        orientatore.nomeIndirizzo = orientatore.indirizzo.nome
        return orientatore
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@orientatori_router.post("/", response_model=OrientatoreResponse)
async def create_orientatore(orientatore: OrientatoreCreate, db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Crea un'orientatore nel database
    """

    if not db.query(Indirizzo).filter(Indirizzo.id == orientatore.indirizzo_id).first():
        raise HTTPException(status_code=404, detail="Indirizzo not found")

    codice = crea_codice_orientatore()

    db_orientatore = Orientatore(
        nome=orientatore.nome,
        cognome=orientatore.cognome,
        email=orientatore.email,
        classe=orientatore.classe,
        indirizzo_id=orientatore.indirizzo_id,
        codice=codice
    )

    db.add(db_orientatore)
    db.commit()
    db.refresh(db_orientatore)
    OrientatoreResponse = db_orientatore
    OrientatoreResponse.nomeIndirizzo = db_orientatore.indirizzo.nome
    return OrientatoreResponse


@orientatori_router.put("/{orientatore_id}", response_model=OrientatoreBaseAdmin)
async def update_orientatore(orientatore_id: int, orientatore_update: OrientatoreUpdate, db: Session = Depends(get_db),
                             _=Depends(admin_access)):
    """
    Aggiorna un'orientatore nel database
    """

    if not db.query(Indirizzo).filter(Indirizzo.id == orientatore_update.indirizzo_id).first():
        raise HTTPException(status_code=404, detail="Indirizzo not found")

    db_orientatore = db.query(Orientatore).filter(Orientatore.id == orientatore_id).first()

    if not db_orientatore:
        raise HTTPException(status_code=404, detail="Orientatore not found")

    if orientatore_update.nome is not None:
        db_orientatore.nome = orientatore_update.nome
    if orientatore_update.cognome is not None:
        db_orientatore.cognome = orientatore_update.cognome
    if orientatore_update.email is not None:
        db_orientatore.email = orientatore_update.email
    if orientatore_update.classe is not None:
        db_orientatore.classe = orientatore_update.classe
    if orientatore_update.indirizzo_id is not None:
        db_orientatore.indirizzo_id = orientatore_update.indirizzo_id

    db.commit()
    db.refresh(db_orientatore)

    return db_orientatore


@orientatori_router.delete("/{orientatore_id}")
async def delete_orientatore(orientatore_id: int, db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Cancella un'orientatore dal database
    """
    if not db.query(Orientatore).filter(Orientatore.id == orientatore_id).first():
        raise HTTPException(status_code=404, detail="Orientatore not found")
    try:
        db.query(Orientatore).filter(Orientatore.id == orientatore_id).delete()
        db.commit()
        return {"message": "Orientatore deleted successfully"}
    except Exception as e:
        if e.args[0] == 1451:
            raise HTTPException(status_code=400, detail="Orientatore has dependencies")
        else:
            raise HTTPException(status_code=500, detail="Internal server error")
