from sqlalchemy import create_engine
from dotenv import load_dotenv
import os


from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models.persona import Persona
from models.trainer import Trainer
from models.alumne import Alumne
from schemas.persona import PersonaOut, PersonaIn, PersonaInsert
from schemas.trainer import TrainerOut, TrainerIn, TrainerInsert
from schemas.alumne import AlumneIn, AlumneOut
from database import get_db
from typing import List

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
    
    persona_model = Persona(**PersonaInsertada.dict())
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

    nou_trainer = Trainer(**trainer_data.dict())
    db.add(nou_trainer)
    db.commit()
    db.refresh(nou_trainer)

    return nou_trainer

#-----------------------------ENDPOINTS PER ELS ALUMNES--------------------------------------------------------

@app.get("/alumnes", response_model=AlumneOut)
def get_all_alumnes(db: Session = Depends(get_db)):
    return db.query(Alumne).first()

@app.post("/alumneName", response_model=AlumneOut)
def get_one_trainer(AlumneCercat: AlumneIn, db: Session = Depends(get_db)):
    return  db.query(Alumne).filter(Alumne.usuari == AlumneCercat.usuari).first()

@app.post("/alumneInsert", response_model=AlumneOut)
def insert_trainer(alumne_data: AlumneIn, db: Session = Depends(get_db)):

    if db.query(Alumne).filter_by(usuari=alumne_data.usuari).first():
        raise HTTPException(status_code=400, detail="Alumne ja existeix")
    
    if db.query(Trainer).filter_by(usuari=alumne_data.usuari).first():
        raise HTTPException(status_code=400, detail="Usuari ja existeix com trainer")

    if not db.query(Persona).filter_by(usuari=alumne_data.usuari).first():
        raise HTTPException(status_code=404, detail="Usuari no trobat a persona")

    nou_alumne = Alumne(**alumne_data.dict())
    db.add(nou_alumne)
    db.commit()
    db.refresh(nou_alumne)

    return nou_alumne

#-------------------------------------------------------------------------------------
