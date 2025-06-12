from sqlalchemy import Column, String
from database import Base  # Asegúrate de que usas la base común

class TutorLegal(Base):
    __tablename__ = "tutor_legal"
    __table_args__ = {"schema": "logiscool"}

    dni = Column(String, primary_key=True, nullable=False)
    nom = Column(String, nullable=False)
    telefon = Column(String, nullable=False)
    email = Column(String, nullable=False)
