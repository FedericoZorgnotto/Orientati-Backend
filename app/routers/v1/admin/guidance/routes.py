from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.route import Route
from app.schemas.route import RouteBase, RouteCreate, RouteUpdate, RouteList

routes_router = APIRouter()


@routes_router.get("/rooms", response_model=RouteList)
async def get_routes(db: Session = Depends(get_db)):
    routes = db.query(Route).all()
    return {"data": routes}


@routes_router.get("/rooms/{route_id}", response_model=RouteBase)
async def get_route(route_id: int, db: Session = Depends(get_db)):
    route = db.query(Route).filter(Route.id == route_id).first()
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    return route


@routes_router.post("/rooms", response_model=RouteBase)
async def create_route(route: RouteCreate, db: Session = Depends(get_db)):
    db_route = Route(
        name=route.name
    )

    db.add(db_route)
    db.commit()
    db.refresh(db_route)
    return db_route


@routes_router.put("/rooms/{route_id}", response_model=RouteBase)
async def update_route(route_id: int, route: RouteUpdate, db: Session = Depends(get_db)):
    db_route = db.query(Route).filter(Route.id == route_id).first()
    if not db_route:
        raise HTTPException(status_code=404, detail="Route not found")
    db_route.name = route.name
    db.commit()
    return db_route


@routes_router.delete("/rooms/{route_id}")
async def delete_route(route_id: int, db: Session = Depends(get_db)):
    db_route = db.query(Route).filter(Route.id == route_id).first()
    if not db_route:
        raise HTTPException(status_code=404, detail="Route not found")
    db.delete(db_route)
    db.commit()
    return {"message": "Route deleted successfully"}
