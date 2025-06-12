from pydantic import BaseModel, EmailStr, Field

class TutorLegalBase(BaseModel):
    dni: str 
    nom: str 
    telefon: str 
    email: str 

class TutorLegalIn(TutorLegalBase):
    pass

class TutorLegalOut(TutorLegalBase):
    class Config:
        orm_mode = True

class TutorCerca(BaseModel):
    dni: str
