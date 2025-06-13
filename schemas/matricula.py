from pydantic import BaseModel
from typing import Optional
from datetime import date
from decimal import Decimal

class MatriculaBase(BaseModel):
    data_ini: date
    data_fi: date
    estat: str
    preu: Decimal
    descompte: Decimal
    nota: Optional[Decimal] = None
    comentari_trainer: Optional[str] = None

class MatriculaIn(MatriculaBase):
    alumne_user: str
    grup_id: int

class MatriculaUpdate(BaseModel):
    data_fi: Optional[date] = None
    estat: Optional[str] = None
    preu: Optional[Decimal] = None
    descompte: Optional[Decimal] = None
    nota: Optional[Decimal] = None
    comentari_trainer: Optional[str] = None

class MatriculaOut(MatriculaBase):
    alumne_user: str
    grup_id: int

    class Config:
        orm_mode = True
