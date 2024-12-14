import csv

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from app.database import get_db
from app.middlewares.auth_middleware import admin_access
from app.models import ScuolaDiProvenienza, Gruppo
from app.models.orientato import Orientato
from app.schemas.orientato import OrientatoList, OrientatoBaseAdmin, OrientatoCreate, OrientatoUpdate, OrientatoResponse

orientati_router = APIRouter()


@orientati_router.get("/", response_model=OrientatoList)
async def get_all_orientati(db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Legge tutti gli orientati dal database
    """

    OrientatoList.orientati = db.query(Orientato).all()
    for orientato in OrientatoList.orientati:
        orientato.nomeScuolaDiProvenienza = orientato.scuolaDiProvenienza.nome
    return OrientatoList


@orientati_router.get("/{orientato_id}", response_model=OrientatoResponse)
async def get_orientato(orientato_id: int, db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Legge un'orientato dal database
    """
    if not db.query(Orientato).filter(Orientato.id == orientato_id).first():
        raise HTTPException(status_code=404, detail="Orientato not found")
    try:
        orientato = db.query(Orientato).filter(Orientato.id == orientato_id).first()
        orientato.nomeScuolaDiProvenienza = orientato.scuolaDiProvenienza.nome
        return orientato
    except Exception as e:  # noqa: F841
        raise HTTPException(status_code=500, detail="Internal server error")


@orientati_router.post("/", response_model=OrientatoResponse)
async def create_orientato(orientato: OrientatoCreate, db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Crea un'orientato nel database
    """

    if not db.query(ScuolaDiProvenienza).filter(ScuolaDiProvenienza.id == orientato.scuolaDiProvenienza_id).first():
        raise HTTPException(status_code=404, detail="ScuolaDiProvenienza not found")

    db_orientato = Orientato(
        nome=orientato.nome,
        cognome=orientato.cognome,
        scuolaDiProvenienza_id=orientato.scuolaDiProvenienza_id
    )

    db.add(db_orientato)
    db.commit()
    db.refresh(db_orientato)
    OrientatoResponse = db_orientato
    OrientatoResponse.nomeScuolaDiProvenienza = db_orientato.scuolaDiProvenienza.nome
    return OrientatoResponse


@orientati_router.put("/{orientato_id}", response_model=OrientatoBaseAdmin)
async def update_orientato(orientato_id: int, orientato_update: OrientatoUpdate, db: Session = Depends(get_db),
                           _=Depends(admin_access)):
    """
    Aggiorna un'orientato nel database
    """

    if not db.query(ScuolaDiProvenienza).filter(
            ScuolaDiProvenienza.id == orientato_update.scuolaDiProvenienza_id).first():
        raise HTTPException(status_code=404, detail="ScuolaDiProvenienza not found")

    db_orientato = db.query(Orientato).filter(Orientato.id == orientato_id).first()

    if not db_orientato:
        raise HTTPException(status_code=404, detail="Orientato not found")

    if orientato_update.nome is not None:
        db_orientato.nome = orientato_update.nome
    if orientato_update.cognome is not None:
        db_orientato.cognome = orientato_update.cognome
    if orientato_update.scuolaDiProvenienza_id is not None:
        db_orientato.scuolaDiProvenienza_id = orientato_update.scuolaDiProvenienza_id

    db.commit()
    db.refresh(db_orientato)

    return db_orientato


@orientati_router.delete("/{orientato_id}")
async def delete_orientato(orientato_id: int, db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Cancella un'orientato dal database
    """
    if not db.query(Orientato).filter(Orientato.id == orientato_id).first():
        raise HTTPException(status_code=404, detail="Orientato not found")
    try:
        db.query(Orientato).filter(Orientato.id == orientato_id).delete()
        db.commit()
        return {"message": "Orientato deleted successfully"}
    except Exception as e:
        if e.args[0] == 1451:
            raise HTTPException(status_code=400, detail="Orientato has dependencies")
        else:
            raise HTTPException(status_code=500, detail="Internal server error")


@orientati_router.post("/upload", response_model=OrientatoList)
async def upload_orientati(file: UploadFile = File(...), db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Carica gli orientati da un file csv
    intestazione del file csv: nome, (cognome), scuolaDiProvenienza_id, turno, data
    """
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Il file deve essere in formato csv")

    content = await file.read()
    decoded_content = content.decode("utf-8", errors="ignore").splitlines()
    
    delimiter = ',' if ',' in decoded_content[0] else ';'
    reader = csv.DictReader(decoded_content, delimiter=delimiter)

    if not all(field in reader.fieldnames for field in ["nome", "turno", "data"]):
        raise HTTPException(status_code=400, detail="Il file deve contenere i campi: nome, turno, data")

    scuolaDiProvenienza_temp = 1

    orientati = []
    for row in reader:
        if "cognome" in reader.fieldnames:

            orientato = Orientato(
                nome=row["nome"],
                cognome=row["cognome"]
            )
        else:
            orientato = Orientato(
                nome=row["nome"],
                cognome=""
            )
        if "scuolaDiProvenienza_id" in reader.fieldnames:
            orientato.scuolaDiProvenienza_id = row["scuolaDiProvenienza_id"]
        else:
            orientato.scuolaDiProvenienza_id = scuolaDiProvenienza_temp

        if not db.query(ScuolaDiProvenienza).filter(
                ScuolaDiProvenienza.id == orientato.scuolaDiProvenienza_id).first():
            if ("scuolaDiProvenienza_id" in reader.fieldnames):
                raise HTTPException(status_code=404, detail="ScuolaDiProvenienza not found with id: " + str(
                    orientato.scuolaDiProvenienza_id))
            else:
                scuola = ScuolaDiProvenienza(
                    nome="SCUOLA",
                    citta="CITTA",
                )
                db.add(scuola)
                db.commit()
                db.refresh(scuola)
                orientato.scuolaDiProvenienza_id = scuola.id
                scuolaDiProvenienza_temp = scuola.id

        if "turno" in reader.fieldnames and "data" in reader.fieldnames:
            if not row["turno"] == "":  # soluzione momentanea per gli orientati che non hanno un turno in ITIS
                db_gruppo = db.query(Gruppo).filter(Gruppo.nome == row["turno"].upper(),
                                                    Gruppo.data == row["data"]).first()
                if not db_gruppo:
                    raise HTTPException(status_code=404,
                                        detail="Gruppo not found with name: " + row["turno"].upper() + " and data: " +
                                               row["data"])
                db_gruppo.orientati.append(orientato)
                db.commit()

        orientati.append(orientato)

    db.add_all(orientati)
    db.commit()

    orientati_list = []
    for orientato in orientati:
        temp = OrientatoResponse(
            id=orientato.id,
            nome=orientato.nome,
            cognome=orientato.cognome,
            scuolaDiProvenienza_id=orientato.scuolaDiProvenienza_id,
            nomeScuolaDiProvenienza=orientato.scuolaDiProvenienza.nome
        )
        orientati_list.append(temp)

    return OrientatoList(orientati=orientati_list)
