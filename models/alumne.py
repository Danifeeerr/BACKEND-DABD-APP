from sqlalchemy import Column, String, Date, ForeignKey
from database import Base

class Alumne(Base):
    __tablename__ = "alumne"
    __table_args__ = {"schema": "logiscool"}

    usuari = Column(String, ForeignKey("logiscool.persona.usuari", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
    data_naixement = Column(Date, nullable=False)
    escola = Column(String, nullable=True)
    dni_tutor = Column(String, ForeignKey("logiscool.tutor_legal.dni", onupdate="CASCADE", ondelete="CASCADE"), nullable=True)
