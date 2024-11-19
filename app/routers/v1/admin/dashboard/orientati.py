from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.middlewares.auth_middleware import admin_access
from app.models import Gruppo
from app.schemas.dashboard.orientato import OrientatoList

Orientati_router = APIRouter()


# @Orientati_router.get("/", response_model=OrientatoList)
# async def get_all_orientati(db: Session = Depends(get_db), _=Depends(admin_access)):
#     """
#     Legge tutti gli orientati dei gruppi che hanno data odierna
#     """
#
#     gruppi = db.query(Gruppo).filter(Gruppo.data == datetime.now().strftime("%Y-%m-%d")).all()
#     orientati: OrientatoList = []
#     for gruppo in gruppi:
#         orientati = gruppo.orientati
#         for orientato in orientati:
#             if orientato not in orientati:
#
#
#         orientati.extend(gruppo.orientati)
#
#     return OrientatoList(orientati=orientati)

