from pydantic import BaseModel

# Esquema de entrada (por ejemplo, para insertar un aula)
class AulaIn(BaseModel):
    numero: int
    capacitat: int

# Esquema de salida (para mostrar un aula, necesita orm_mode)
class AulaOut(BaseModel):
    numero: int
    capacitat: int

    class Config:
        orm_mode = True
