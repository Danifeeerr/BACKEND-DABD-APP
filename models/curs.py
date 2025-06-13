from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from database import Base

class Curs(Base):
    __tablename__ = "curs"
    __table_args__ = {"schema": "logiscool"}

    codi = Column(String, primary_key=True)
