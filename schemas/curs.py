from pydantic import BaseModel

class CursBase(BaseModel):
    codi: str

class CursIn(CursBase):
    pass

class CursOut(CursBase):
    class Config:
        orm_mode = True
