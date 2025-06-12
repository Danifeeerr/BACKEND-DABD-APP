from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Aula(Base):
    __tablename__ = "aula"
    __table_args__ = {"schema": "logiscool"}

    numero = Column(Integer, primary_key=True, nullable=False)
    capacitat = Column(Integer, nullable=False)
