from pydantic import BaseModel

class PersonaIn(BaseModel):
    usuari: str

    class Config:
        orm_mode = True

class PersonaOut(BaseModel):
    usuari: str

    class Config:
        orm_mode = True

class PersonaInsert(BaseModel):
    usuari: str
    contrassenya: str

    class Config:
        orm_mode = True
