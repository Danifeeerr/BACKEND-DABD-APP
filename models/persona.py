from sqlalchemy import Column, String
from database import Base

class Persona(Base):
    __tablename__ = "persona"
    __table_args__ = {"schema": "logiscool"}

    usuari = Column(String, primary_key=True)
    contrassenya = Column(String, nullable=False)
