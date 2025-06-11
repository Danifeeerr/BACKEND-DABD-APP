from sqlalchemy import Column, String, Numeric, ForeignKey
from database import Base


class Trainer(Base):
    __tablename__ = "trainer"
    __table_args__ = {"schema": "logiscool"}

    usuari = Column(String, ForeignKey("logiscool.persona.usuari", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
    correu = Column(String, nullable=False)
    sou_hora = Column(Numeric(10, 2), nullable=False)
