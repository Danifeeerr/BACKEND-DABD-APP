from datetime import time
from pydantic import BaseModel
from typing import Optional

class GrupBase(BaseModel):
    dia_setmanal: str
    hora_ini: time
    hora_fi: time
    codi_curs: Optional[str] = None
    trainer_assignat: Optional[str] = None
    aula_numero: Optional[int] = None

class GrupIn(GrupBase):
    pass

class GrupUpdate(BaseModel):
    dia_setmanal: Optional[str] = None
    hora_ini: Optional[time] = None
    hora_fi: Optional[time] = None
    codi_curs: Optional[str] = None
    trainer_assignat: Optional[str] = None
    aula_numero: Optional[int] = None

class GrupOut(GrupBase):
    id: int

    class Config:
        orm_mode = True