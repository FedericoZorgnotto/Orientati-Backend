from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.middlewares.auth_middleware import admin_access
from app.models import Gruppo, Orientato, Presente
from app.schemas.dashboard.orientato import OrientatoList, OrientatoBase

orientati_router = APIRouter()


@orientati_router.get("/", response_model=OrientatoList)
async def get_all_orientati(db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Legge tutti gli orientati dei gruppi che hanno data odierna, orientati per presenza
    """

    gruppi = db.query(Gruppo).filter(Gruppo.data == datetime.now().strftime("%d/%m/%Y")).all()
    orientati = []
    for gruppo in gruppi:
        for orientato in gruppo.orientati:
            presente = False
            for orientatoPresente in gruppo.presenti:
                if orientatoPresente.orientato_id == orientato.id:
                    presente = True
                    break
            assente = False
            for orientatoAssente in gruppo.assenti:
                if orientatoAssente.orientato_id == orientato.id:
                    assente = True
                    break

            oraPartenza = ""
            if gruppo.numero_tappa == 0 and gruppo.arrivato is False:
                oraPartenza = gruppo.orario_partenza

            orientati.append(OrientatoBase(
                id=orientato.id,
                nome=orientato.nome,
                cognome=orientato.cognome,
                scuolaDiProvenienza_nome=orientato.scuolaDiProvenienza.nome,
                presente=presente,
                assente=assente,
                gruppo_id=gruppo.id,
                gruppo_nome=gruppo.nome,
                gruppo_orario_partenza=oraPartenza
            ))

    # ordinamento per presenza e assenza, prima quelli non presenti e non assenti,
    # al fondo i presenti seguiti da quelli assenti
    orientati = sorted(orientati, key=lambda orientato: orientato.presente)
    orientati = sorted(orientati, key=lambda orientato: orientato.assente)
    return OrientatoList(orientati=orientati)


@orientati_router.put("/{orientato_id}")
async def update_orientato(orientato_id: int, presente: bool, assente: bool, db: Session = Depends(get_db),
                           _=Depends(admin_access)):
    """
    Segna un orientato come presente o assente al primo gruppo di oggi
    """
    orientato = db.query(Orientato).filter(Orientato.id == orientato_id).first()
    if not orientato:
        raise HTTPException(status_code=404, detail="Orientato not found")

    gruppo = db.query(Gruppo).filter(Gruppo.data == datetime.now().strftime("%d/%m/%Y"),
                                     Gruppo.orientati.any(id=orientato_id)).first()
    if not gruppo:
        raise HTTPException(status_code=404, detail="Gruppo not found for the given orientato")

    if presente and assente:
        raise HTTPException(status_code=400, detail="You can't be present and absent at the same time")

    def elimina_presente(orientato_id):
        for orientatoPresente in gruppo.presenti:
            if orientatoPresente.orientato_id == orientato_id:
                db.delete(orientatoPresente)
                break

    def elimina_assente(orientato_id):
        for orientatoAssente in gruppo.assenti:
            if orientatoAssente.orientato_id == orientato_id:
                db.delete(orientatoAssente)
                break

    if presente:
        gruppo.presenti.append(Presente(orientato_id=orientato_id))
        elimina_assente(orientato_id)

    elif assente:
        gruppo.assenti.append(Presente(orientato_id=orientato_id))
        elimina_presente(orientato_id)
    else:
        elimina_assente(orientato_id)
        elimina_presente(orientato_id)

    db.commit()
    return {"message": "Orientato updated successfully"}
