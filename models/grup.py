from sqlalchemy import Column, Integer, String, Time, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Grup(Base):
    __tablename__ = "grup"
    __table_args__ = {"schema": "logiscool"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    dia_setmanal = Column(String, nullable=False)
    hora_ini = Column(Time, nullable=False)
    hora_fi = Column(Time, nullable=False)
    codi_curs = Column(String, ForeignKey("logiscool.curs.codi", onupdate="CASCADE", ondelete="SET NULL"), nullable=True)
    trainer_assignat = Column(String, ForeignKey("logiscool.trainer.usuari", onupdate="CASCADE", ondelete="SET NULL"), nullable=True)
    aula_numero = Column(Integer, ForeignKey("logiscool.aula.numero", onupdate="CASCADE", ondelete="SET NULL"), nullable=True)
