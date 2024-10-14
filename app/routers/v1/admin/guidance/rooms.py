from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.middlewares.auth_middleware import admin_access
from app.models.room import Room
from app.schemas.room import RoomBase, RoomCreate, RoomUpdate, RoomList

rooms_router = APIRouter()


@rooms_router.get("/rooms", response_model=RoomList)
async def get_all_rooms(db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Legge tutte le stanze dal database
    """

    RoomList.rooms = db.query(Room).all()
    return RoomList


@rooms_router.get("/rooms/{room_id}", response_model=RoomBase)
async def get_room(room_id: int, db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Legge una stanza dal database
    """
    if not db.query(Room).filter(Room.id == room_id).first():
        raise HTTPException(status_code=404, detail="Room not found")
    try:
        room = db.query(Room).filter(Room.id == room_id).first()
        return room
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@rooms_router.post("/rooms", response_model=RoomBase)
async def create_room(room: RoomCreate, db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Crea una stanza nel database
    """

    db_room = Room(
        name=room.name,
        args=room.args,
        specialisation_id=room.specialisation_id
    )

    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room


@rooms_router.put("/rooms/{room_id}", response_model=RoomBase)
async def update_room(room_id: int, room: RoomUpdate, db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Aggiorna una stanza nel database
    """
    if not db.query(Room).filter(Room.id == room_id).first():
        raise HTTPException(status_code=404, detail="Room not found")
    try:
        db_room = db.query(Room).filter(Room.id == room_id).first()
        db_room.name = room.name
        db_room.args = room.args
        db_room.specialisation_id = room.specialisation_id
        db.commit()
        db.refresh(db_room)
        return db_room
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@rooms_router.delete("/rooms/{room_id}")
async def delete_room(room_id: int, db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Cancella una stanza dal database
    """
    db_room = db.query(Room).filter(Room.id == room_id).first()

    if not db_room:
        raise HTTPException(status_code=404, detail="Room not found")
    try:
        db.delete(db_room)
        db.commit()
        return {"message": "Room deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
