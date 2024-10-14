from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.middlewares.auth_middleware import admin_access
from app.models.group import Group
from app.schemas.group import GroupBase, GroupCreate, GroupUpdate, GroupList

groups_router = APIRouter()


@groups_router.get("/groups", response_model=GroupList)
async def get_all_groups(db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Read all groups from the database
    """

    GroupList.groups = db.query(Group).join(Group.users).join(Group.route).all()
    return GroupList


@groups_router.get("/groups/{group_id}", response_model=GroupBase)
async def get_group(group_id: int, db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Read a group from the database
    """
    if not db.query(Group).filter(Group.id == group_id).first():
        raise HTTPException(status_code=404, detail="Group not found")
    try:
        group = db.query(Group).filter(Group.id == group_id).join(Group.users).join(Group.route).first()
        return group
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@groups_router.post("/groups", response_model=GroupBase)
async def create_group(group: GroupCreate, db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Create a group in the database
    """

    db_group = Group(
        start_hour=group.start_hour,
        notes=group.notes,
        stage_number=group.stage_number,
        is_arrived=group.is_arrived,
        route_id=group.route_id
    )

    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group


@groups_router.put("/groups/{group_id}", response_model=GroupBase)
async def update_group(group_id: int, group: GroupUpdate, db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Update a group in the database
    """
    if not db.query(Group).filter(Group.id == group_id).first():
        raise HTTPException(status_code=404, detail="Group not found")
    try:
        db_group = db.query(Group).filter(Group.id == group_id).first()
        db_group.start_hour = group.start_hour
        db_group.notes = group.notes
        db_group.stage_number = group.stage_number
        db_group.is_arrived = group.is_arrived
        db_group.route_id = group.route_id
        db.commit()
        db.refresh(db_group)
        return db_group
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@groups_router.delete("/groups/{group_id}")
async def delete_group(group_id: int, db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Delete a group from the database
    """
    if not db.query(Group).filter(Group.id == group_id).first():
        raise HTTPException(status_code=404, detail="Group not found")
    try:
        db.query(Group).filter(Group.id == group_id).delete()
        db.commit()
        return {"message": "Group deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
