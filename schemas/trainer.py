from pydantic import BaseModel
from decimal import Decimal

class TrainerOut(BaseModel):
    usuari: str
    correu: str
    sou_hora: Decimal

    class Config:
        orm_mode = True

class TrainerIn(BaseModel):
    usuari: str

    class Config:
        orm_mode = True