from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.middlewares.auth_middleware import admin_access
from app.models import Gruppo, Presente, Assente, FasciaOraria, Ragazzo, Data, Iscrizione

ragazzi_router = APIRouter()


@ragazzi_router.put("/{ragazzo_id}")
async def update_ragazzo(ragazzo_id: int, gruppo_id: int, presente: bool, assente: bool, db: Session = Depends(get_db),
                         _=Depends(admin_access)):
    """
    Segna un ragazzo come presente o assente al primo gruppo di oggi
    """
    ragazzo = db.query(Ragazzo).join(Ragazzo.iscrizioni).filter(Ragazzo.id == ragazzo_id).first()
    if not ragazzo:
        raise HTTPException(status_code=404, detail="Ragazzo not found")

    gruppo = db.query(Gruppo).join(Gruppo.fasciaOraria).join(FasciaOraria.data).filter(Gruppo.id == gruppo_id).first()
    if not gruppo:
        raise HTTPException(status_code=404, detail="Gruppo not found for the given id")

    if presente and assente:
        raise HTTPException(status_code=400, detail="You can't be present and absent at the same time")

    def elimina_presente(ragazzo_id):
        for ragazzoPresente in gruppo.presenti:
            if ragazzoPresente.ragazzo_id == ragazzo_id:
                db.delete(ragazzoPresente)
                break

    def elimina_assente(ragazzo_id):
        for ragazzoAssente in gruppo.assenti:
            if ragazzoAssente.ragazzo_id == ragazzo_id:
                db.delete(ragazzoAssente)
                break

    if presente:
        gruppo.presenti.append(Presente(ragazzo_id=ragazzo_id))
        elimina_assente(ragazzo_id)
    elif assente:
        gruppo.assenti.append(Assente(ragazzo_id=ragazzo_id))
        elimina_presente(ragazzo_id)
    else:
        elimina_assente(ragazzo_id)
        elimina_presente(ragazzo_id)

    db.commit()
    return {"message": "Ragazzo updated successfully"}
