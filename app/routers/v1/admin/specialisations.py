from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.middlewares.auth_middleware import admin_access
from app.models.specialisation import Specialisation
from app.schemas.specialisation import SpecialisationBase, SpecialisationCreate, SpecialisationUpdate, \
    SpecialisationList

specialisations_router = APIRouter()


@specialisations_router.get("/specialisations", response_model=SpecialisationList)
async def get_all_specialisations(db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Legge tutte le specializzazioni dal database
    """

    SpecialisationList.specialisations = db.query(Specialisation).all()
    return SpecialisationList


@specialisations_router.get("/specialisations/{specialisation_id}", response_model=SpecialisationBase)
async def get_specialisation(specialisation_id: int, db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Legge una specializzazione dal database
    """
    if not db.query(Specialisation).filter(Specialisation.id == specialisation_id).first():
        raise HTTPException(status_code=404, detail="Specialisation not found")
    try:
        specialisation = db.query(Specialisation).filter(Specialisation.id == specialisation_id).first()
        return specialisation
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@specialisations_router.post("/specialisations", response_model=SpecialisationBase)
async def create_specialisation(specialisation: SpecialisationCreate, db: Session = Depends(get_db),
                                _=Depends(admin_access)):
    """
    Crea una specializzazione nel database
    """

    db_specialisation = Specialisation(
        name=specialisation.name
    )

    db.add(db_specialisation)
    db.commit()
    db.refresh(db_specialisation)
    return db_specialisation


@specialisations_router.put("/specialisations/{specialisation_id}", response_model=SpecialisationBase)
async def update_specialisation(specialisation_id: int, specialisation: SpecialisationUpdate,
                                db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Aggiorna una specializzazione nel database
    """
    if not db.query(Specialisation).filter(Specialisation.id == specialisation_id).first():
        raise HTTPException(status_code=404, detail="Specialisation not found")
    try:
        db_specialisation = db.query(Specialisation).filter(Specialisation.id == specialisation_id).first()
        db_specialisation.name = specialisation.name
        db_specialisation.users = specialisation.users
        db_specialisation.rooms = specialisation.rooms
        db.commit()
        db.refresh(db_specialisation)
        return db_specialisation
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@specialisations_router.delete("/specialisations/{specialisation_id}")
async def delete_specialisation(specialisation_id: int, db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Cancella una specializzazione dal database
    """
    if not db.query(Specialisation).filter(Specialisation.id == specialisation_id).first():
        raise HTTPException(status_code=404, detail="Specialisation not found")
    try:
        db.query(Specialisation).filter(Specialisation.id == specialisation_id).delete()
        db.commit()
        return {"message": "Specialisation deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
