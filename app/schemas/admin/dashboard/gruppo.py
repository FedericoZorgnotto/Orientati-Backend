from __future__ import annotations
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class GruppoBase(BaseModel):
    nome: str
    codice: Optional[str] = None
    fasciaOraria_id: int
    numero_tappa: Optional[int] = None
    arrivato: Optional[bool] = None
    orario_partenza_effettivo: Optional[str] = None
    orario_fine_effettivo: Optional[str] = None
    percorsoFinito: Optional[bool] = None
    aula_nome: Optional[str] = None
    aula_posizione: Optional[str] = None
    aula_materia: Optional[str] = None
    minuti_arrivo: Optional[int] = None
    minuti_partenza: Optional[int] = None
    totale_orientati: Optional[int] = None
    orientati_presenti: Optional[int] = None
    orientati_assenti: Optional[int] = None


class GruppoResponse(GruppoBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class GruppoStatisticheResponse(BaseModel):
    nome: str
    orario_partenza_effettivo: Optional[str] = None
    orario_fine_effettivo: Optional[str] = None


class GruppoList(BaseModel):
    gruppi: List[GruppoResponse]


class GruppoStatisticheList(BaseModel):
    gruppi: List[GruppoStatisticheResponse]