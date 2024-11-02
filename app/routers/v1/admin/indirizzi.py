from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.middlewares.auth_middleware import admin_access
from app.models import PercorsoDiStudi
from app.models.indirizzo import Indirizzo
from app.schemas.indirizzo import IndirizzoList, IndirizzoBaseAdmin, IndirizzoCreate, IndirizzoUpdate, IndirizzoResponse

indirizzi_router = APIRouter()


@indirizzi_router.get("/", response_model=IndirizzoList)
async def get_all_indirizzi(db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Legge tutti gli indirizzi dal database
    """

    IndirizzoList.indirizzi = (db.query(Indirizzo).all())
    for indirizzo in IndirizzoList.indirizzi:
        indirizzo.nomePercorsoDiStudi = indirizzo.percorsoDiStudi.nome
    return IndirizzoList


@indirizzi_router.get("/{indirizzo_id}", response_model=IndirizzoResponse)
async def get_indirizzo(indirizzo_id: int, db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Legge un'indirizzo dal database
    """
    if not (db.query(Indirizzo).filter(Indirizzo.id == indirizzo_id).first()):
        raise HTTPException(status_code=404, detail="Indirizzo not found")
    try:
        indirizzo = db.query(Indirizzo).filter(Indirizzo.id == indirizzo_id).first()
        indirizzo.nomePercorsoDiStudi = indirizzo.percorsoDiStudi.nome
        return indirizzo
    except Exception as e:  # noqa: F841
        raise HTTPException(status_code=500, detail="Internal server error")


@indirizzi_router.post("/", response_model=IndirizzoResponse)
async def create_indirizzo(indirizzo: IndirizzoCreate, db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Crea un'indirizzo nel database
    """

    if not db.query(PercorsoDiStudi).filter(PercorsoDiStudi.id == indirizzo.percorsoDiStudi_id).first():
        raise HTTPException(status_code=404, detail="PercorsoDiStudi not found")

    db_indirizzo = Indirizzo(
        nome=indirizzo.nome,
        percorsoDiStudi_id=indirizzo.percorsoDiStudi_id
    )

    db.add(db_indirizzo)
    db.commit()
    db.refresh(db_indirizzo)
    IndirizzoResponse = db_indirizzo
    IndirizzoResponse.nomePercorsoDiStudi = db_indirizzo.percorsoDiStudi.nome
    return IndirizzoResponse


@indirizzi_router.put("/{indirizzo_id}", response_model=IndirizzoBaseAdmin)
async def update_indirizzo(indirizzo_id: int, indirizzo_update: IndirizzoUpdate, db: Session = Depends(get_db),
                           _=Depends(admin_access)):
    """
    Aggiorna un'indirizzo nel database
    """

    if not db.query(PercorsoDiStudi).filter(PercorsoDiStudi.id == indirizzo_update.percorsoDiStudi_id).first():
        raise HTTPException(status_code=404, detail="PercorsoDiStudi not found")

    db_indirizzo = db.query(Indirizzo).filter(Indirizzo.id == indirizzo_id).first()

    if not db_indirizzo:
        raise HTTPException(status_code=404, detail="Indirizzo not found")

    if indirizzo_update.nome is not None:
        db_indirizzo.nome = indirizzo_update.nome
    if indirizzo_update.percorsoDiStudi_id is not None:
        db_indirizzo.percorsoDiStudi_id = indirizzo_update.percorsoDiStudi_id

    db.commit()
    db.refresh(db_indirizzo)

    return db_indirizzo


@indirizzi_router.delete("/{indirizzo_id}")
async def delete_indirizzo(indirizzo_id: int, db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Cancella un'indirizzo dal database
    """
    if not db.query(Indirizzo).filter(Indirizzo.id == indirizzo_id).first():
        raise HTTPException(status_code=404, detail="Indirizzo not found")
    try:
        db.query(Indirizzo).filter(Indirizzo.id == indirizzo_id).delete()
        db.commit()
        return {"message": "Indirizzo deleted successfully"}
    except Exception as e:
        if e.args[0] == 1451:
            raise HTTPException(status_code=400, detail="Indirizzo has dependencies")
        else:
            raise HTTPException(status_code=500, detail="Internal server error")
