from typing import Optional, List

from pydantic import BaseModel, ConfigDict


class GruppoBase(BaseModel):
    nome: str
    orario_partenza: str
    orario_partenza_effettivo: Optional[str] = None
    orario_fine_effettivo: Optional[str] = None
    data: str
    numero_tappa: Optional[int] = None
    arrivato: Optional[bool] = None
    percorsoFinito: Optional[bool] = None
    nomi_orientatori: Optional[List[str]] = None
    aula_nome: Optional[str] = None
    aula_posizione: Optional[str] = None
    aula_materia: Optional[str] = None
    minuti_arrivo: Optional[int] = None
    minuti_partenza: Optional[int] = None
    totale_orientati: Optional[int] = None
    orientati_presenti: Optional[int] = None

class GruppoResponse(GruppoBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class GruppoStatisticheRespone(BaseModel):
    nome: str
    orario_partenza: str
    orario_partenza_effettivo: Optional[str] = None
    orario_fine_effettivo: Optional[str] = None

class GruppoList(BaseModel):
    gruppi: List[GruppoResponse]

class GruppoStatisticheList(BaseModel):
    gruppi: List[GruppoStatisticheRespone]
