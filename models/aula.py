from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from database import Base

class Aula(Base):
    __tablename__ = "aula"
    __table_args__ = {"schema": "logiscool"}

    numero = Column(Integer, primary_key=True, nullable=False)
    capacitat = Column(Integer, nullable=False)
