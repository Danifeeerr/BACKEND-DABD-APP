from sqlalchemy import Column, String, Numeric, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Trainer(Base):
    __tablename__ = "trainer"
    __table_args__ = {"schema": "practica"}

    usuari = Column(String, ForeignKey("practica.persona.usuari", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
    correu = Column(String, nullable=False)
    sou_hora = Column(Numeric(10, 2), nullable=False)
