from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from typing import List

#-----------------------Imports de models--------------------------------------------------------
from models.persona import Persona
from models.trainer import Trainer
from models.alumne import Alumne
from models.aula import Aula
from models.grup import Grup

#-----------------------Imports de schemas--------------------------------------------------------
from models.tutor_legal import TutorLegal
from schemas.persona import PersonaOut, PersonaIn, PersonaInsert
from schemas.trainer import TrainerOut, TrainerIn, TrainerInsert
from schemas.alumne import AlumneIn, AlumneOut
from schemas.tutor_legal import TutorLegalIn, TutorLegalOut, TutorCerca
from schemas.aula import AulaIn, AulaOut
from schemas.grup import GrupIn, GrupUpdate, GrupOut


load_dotenv()

user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
db = os.getenv("DB_NAME")
schema = os.getenv("DB_SCHEMA")

DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{db}"

# Añadir options para el search_path
engine = create_engine(
    DATABASE_URL,
    connect_args={"options": f"-csearch_path={schema},public"}
)


app = FastAPI()

#-----------------------------ENDPOINTS PER LES PERSONES--------------------------------------------------------

@app.get("/persones", response_model=List[PersonaOut])
def get_all_persones(db: Session = Depends(get_db)):
    return db.query(Persona).all()

@app.post("/personaName", response_model=PersonaOut)
def get_one_persona(PersonaCercada: PersonaIn, db: Session = Depends(get_db)):
    return db.query(Persona).filter(Persona.usuari == PersonaCercada.usuari).first()

@app.post("/personaInsert", response_model=PersonaOut)
def insert_persona(PersonaInsertada: PersonaInsert, db: Session = Depends(get_db)):


    if db.query(Persona).filter_by(usuari=PersonaInsertada.usuari).first():
        raise HTTPException(status_code=400, detail="Trainer ja existeix")
    
    persona_model = Persona(**PersonaInsertada.model_dump())
    db.add(persona_model)
    db.commit()
    db.refresh(persona_model)
    return persona_model


#-----------------------------ENDPOINTS PER ELS TRAINERS--------------------------------------------------------

@app.get("/trainers", response_model=List[TrainerOut])
def get_all_trainers(db: Session = Depends(get_db)):
    return db.query(Trainer).all()

@app.post("/trainerName", response_model=TrainerOut)
def get_one_trainer(TrainerCercat: TrainerIn, db: Session = Depends(get_db)):
    return  db.query(Trainer).filter(Trainer.usuari == TrainerCercat.usuari).first()

@app.post("/trainerInsert", response_model=TrainerOut)
def insert_trainer(trainer_data: TrainerInsert, db: Session = Depends(get_db)):

    if db.query(Trainer).filter_by(usuari=trainer_data.usuari).first():
        raise HTTPException(status_code=400, detail="Trainer ja existeix")
    
    if db.query(Alumne).filter_by(usuari=trainer_data.usuari).first():
        raise HTTPException(status_code=400, detail="Usuari ja existeix com alumne")

    if not db.query(Persona).filter_by(usuari=trainer_data.usuari).first():
        raise HTTPException(status_code=404, detail="Usuari no trobat a persona")

    nou_trainer = Trainer(**trainer_data.model_dump())
    db.add(nou_trainer)
    db.commit()
    db.refresh(nou_trainer)

    return nou_trainer

#-----------------------------ENDPOINTS PER ELS ALUMNES--------------------------------------------------------

@app.get("/alumnes", response_model=AlumneOut)
def get_all_alumnes(db: Session = Depends(get_db)):
    return db.query(Alumne).all()

@app.post("/alumneName", response_model=AlumneOut)
def get_one_alumne(AlumneCercat: AlumneIn, db: Session = Depends(get_db)):
    return  db.query(Alumne).filter(Alumne.usuari == AlumneCercat.usuari).first()

@app.post("/alumneInsert", response_model=AlumneOut)
def insert_alumne(alumne_data: AlumneIn, db: Session = Depends(get_db)):

    if db.query(Alumne).filter_by(usuari=alumne_data.usuari).first():
        raise HTTPException(status_code=400, detail="Alumne ja existeix")
    
    if db.query(Trainer).filter_by(usuari=alumne_data.usuari).first():
        raise HTTPException(status_code=400, detail="Usuari ja existeix com trainer")

    if not db.query(Persona).filter_by(usuari=alumne_data.usuari).first():
        raise HTTPException(status_code=404, detail="Usuari no trobat a persona")

    nou_alumne = Alumne(**alumne_data.model_dump())
    db.add(nou_alumne)
    db.commit()
    db.refresh(nou_alumne)

    return nou_alumne

#-----------------------------ENDPOINTS PER ELS TUTORS LEGALS--------------------------------------------------------

@app.get("/tutorslegals", response_model=TutorLegalOut)
def get_all_tutors(db: Session = Depends(get_db)):
    return db.query(TutorLegal).all()

@app.post("/tutorDNI", response_model=TutorLegalOut)
def get_one_tutor(TutorCercat: TutorCerca, db: Session = Depends(get_db)):
    return  db.query(TutorLegal).filter(TutorLegal.dni == TutorCercat.dni).first()

@app.post("/tutorInsert", response_model=TutorLegalOut)
def insert_tutor(tutor_data: TutorLegalIn, db: Session = Depends(get_db)):

    if db.query(TutorLegal).filter_by(dni=tutor_data.dni).first():
        raise HTTPException(status_code=400, detail="Tutor legal ja existeix")

    nou_tutor = TutorLegal(**tutor_data.model_dump())
    db.add(nou_tutor)
    db.commit()
    db.refresh(nou_tutor)

    return nou_tutor

#-----------------------------ENDPOINTS PER LES AULES--------------------------------------------------------
@app.get("/aules", response_model=List[AulaOut])
def get_all_aules(db: Session = Depends(get_db)):
    return db.query(Aula).all()

@app.post("/aulaInsert", response_model=AulaOut)
def insert_aula(aula_data: AulaIn, db: Session = Depends(get_db)):
    if db.query(Aula).filter_by(numero=aula_data.numero).first():
        raise HTTPException(status_code=400, detail="Aula ja existeix")

    nova_aula = Aula(**aula_data.model_dump())
    db.add(nova_aula)
    db.commit()
    db.refresh(nova_aula)

    return nova_aula

@app.post("/aulaNumber", response_model=AulaOut)
def get_aula_by_number(aula_data: AulaIn, db: Session = Depends(get_db)):
    aula = db.query(Aula).filter(Aula.numero == aula_data.numero).first()
    if not aula:
        raise HTTPException(status_code=404, detail="Aula no trobada")
    return aula

#-----------------------------ENDPOINTS PER ELS GRUPS--------------------------------------------------------

