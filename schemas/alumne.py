from pydantic import BaseModel
from datetime import date
from typing import Optional

class AlumneOut(BaseModel):
    usuari: str
    data_naixement: date
    escola: Optional[str]
    dni_tutor: Optional[str]

    class Config:
        orm_mode = True

class AlumneIn(BaseModel):
    usuari: str
    data_naixement: date
    escola: Optional[str] = None
    dni_tutor: Optional[str] = None

