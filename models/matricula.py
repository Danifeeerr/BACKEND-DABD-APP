from sqlalchemy import Column, String, Integer, Date, Numeric, Text, ForeignKey
from database import Base 

class Matricula(Base):
    __tablename__ = "matricula"
    __table_args__ = {"schema": "logiscool"}

    alumne_user = Column(String, ForeignKey("logiscool.persona.usuari", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
    grup_id = Column(Integer, ForeignKey("logiscool.grup.id", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
    data_ini = Column(Date, nullable=False)
    data_fi = Column(Date, nullable=False)
    estat = Column(String, nullable=False)
    preu = Column(Numeric(10, 2), nullable=False)
    descompte = Column(Numeric(10, 2), nullable=False)
    nota = Column(Numeric(4, 2), nullable=True)
    comentari_trainer = Column(Text, nullable=True)
