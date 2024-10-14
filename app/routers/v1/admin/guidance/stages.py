from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.middlewares.auth_middleware import admin_access
from app.models.stage import Stage
from app.schemas.stage import StageBase, StageCreate, StageUpdate, StageList

stages_router = APIRouter()


@stages_router.get("/stages", response_model=StageList)
async def get_stages(db: Session = Depends(get_db), _=Depends(admin_access)):
    stages = db.query(Stage).all()
    return {"data": stages}


@stages_router.get("/stages/{stage_id}", response_model=StageBase)
async def get_stage(stage_id: int, db: Session = Depends(get_db), _=Depends(admin_access)):
    stage = db.query(Stage).filter(Stage.id == stage_id).first()
    if not stage:
        raise HTTPException(status_code=404, detail="Stage not found")
    return stage


@stages_router.post("/stages", response_model=StageBase)
async def create_stage(stage: StageCreate, db: Session = Depends(get_db), _=Depends(admin_access)):
    db_stage = Stage(
        start_minute=stage.start_minute,
        end_minute=stage.end_minute,
        route_id=stage.route_id,
        room_id=stage.room_id
    )

    db.add(db_stage)
    db.commit()
    db.refresh(db_stage)
    return db_stage


@stages_router.put("/stages/{stage_id}", response_model=StageBase)
async def update_stage(stage_id: int, stage: StageUpdate, db: Session = Depends(get_db), _=Depends(admin_access)):
    db_stage = db.query(Stage).filter(Stage.id == stage_id).first()
    if not db_stage:
        raise HTTPException(status_code=404, detail="Stage not found")
    db_stage.start_minute = stage.start_minute
    db_stage.end_minute = stage.end_minute
    db_stage.route_id = stage.route_id
    db_stage.room_id = stage.room_id
    db.commit()
    return db_stage


@stages_router.delete("/stages/{stage_id}")
async def delete_stage(stage_id: int, db: Session = Depends(get_db), _=Depends(admin_access)):
    db_stage = db.query(Stage).filter(Stage.id == stage_id).first()
    if not db_stage:
        raise HTTPException(status_code=404, detail="Stage not found")
    db.delete(db_stage)
    db.commit()
    return {"message": "Stage deleted successfully"}
