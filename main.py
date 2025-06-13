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
from models.tutor_legal import TutorLegal
from models.aula import Aula
from models.grup import Grup
from models.curs import Curs
from models.matricula import Matricula

#-----------------------Imports de schemas--------------------------------------------------------
from schemas.persona import PersonaOut, PersonaIn, PersonaInsert
from schemas.trainer import TrainerOut, TrainerIn, TrainerInsert
from schemas.alumne import AlumneIn, AlumneOut
from schemas.tutor_legal import TutorLegalIn, TutorLegalOut, TutorCerca
from schemas.aula import AulaIn, AulaOut
from schemas.grup import GrupIn, GrupUpdate, GrupOut
from schemas.curs import CursIn, CursOut
from schemas.matricula import MatriculaIn, MatriculaOut, MatriculaUpdate
#-----------------------Configuració de la base de dades--------------------------------------------------------
load_dotenv()

user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
db = os.getenv("DB_NAME")
schema = os.getenv("DB_SCHEMA")

DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{db}"

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

@app.post("/personaDelete/{usuari}")
def delete_persona(usuari: str, db: Session = Depends(get_db)):
    persona = db.query(Persona).filter(Persona.usuari == usuari).first()
    if not persona:
        raise HTTPException(status_code=404, detail="Persona no trobada")

    db.delete(persona)
    db.commit()

    return {"detail": "Persona eliminada correctament"}


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

@app.post("/trainerUpdate/{usuari}", response_model=TrainerOut)
def update_trainer(usuari: str, trainer_data: TrainerIn, db: Session = Depends(get_db)):
    trainer = db.query(Trainer).filter(Trainer.usuari == usuari).first()
    if not trainer:
        raise HTTPException(status_code=404, detail="Trainer no trobat")

    for key, value in trainer_data.model_dump(exclude_unset=True).items():
        setattr(trainer, key, value)

    db.commit()
    db.refresh(trainer)

    return trainer

@app.post("/trainerDelete/{usuari}")
def delete_trainer(usuari: str, db: Session = Depends(get_db)):
    trainer = db.query(Trainer).filter(Trainer.usuari == usuari).first()
    if not trainer:
        raise HTTPException(status_code=404, detail="Trainer no trobat")

    db.delete(trainer)
    db.commit()

    return {"detail": "Trainer eliminat correctament"}

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

@app.post("/alumneUpdate/{usuari}", response_model=AlumneOut)
def update_alumne(usuari: str, alumne_data: AlumneIn, db: Session = Depends(get_db)):
    alumne = db.query(Alumne).filter(Alumne.usuari == usuari).first()
    if not alumne:
        raise HTTPException(status_code=404, detail="Alumne no trobat")

    for key, value in alumne_data.model_dump(exclude_unset=True).items():
        setattr(alumne, key, value)

    db.commit()
    db.refresh(alumne)

    return alumne

@app.post("/alumneDelete/{usuari}")
def delete_alumne(usuari: str, db: Session = Depends(get_db)):
    alumne = db.query(Alumne).filter(Alumne.usuari == usuari).first()
    if not alumne:
        raise HTTPException(status_code=404, detail="Alumne no trobat")

    db.delete(alumne)
    db.commit()

    return {"detail": "Alumne eliminat correctament"}

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

@app.post("/tutorUpdate/{dni}", response_model=TutorLegalOut)
def update_tutor(dni: str, tutor_data: TutorLegalIn, db: Session = Depends(get_db)):
    tutor = db.query(TutorLegal).filter(TutorLegal.dni == dni).first()
    if not tutor:
        raise HTTPException(status_code=404, detail="Tutor legal no trobat")

    for key, value in tutor_data.model_dump(exclude_unset=True).items():
        setattr(tutor, key, value)

    db.commit()
    db.refresh(tutor)

    return tutor

@app.post("/tutorDelete/{dni}")
def delete_tutor(dni: str, db: Session = Depends(get_db)):
    tutor = db.query(TutorLegal).filter(TutorLegal.dni == dni).first()
    if not tutor:
        raise HTTPException(status_code=404, detail="Tutor legal no trobat")

    db.delete(tutor)
    db.commit()

    return {"detail": "Tutor legal eliminat correctament"}

#-----------------------------ENDPOINTS PER LES AULES--------------------------------------------------------
@app.get("/aules", response_model=List[AulaOut])
def get_all_aules(db: Session = Depends(get_db)):
    return db.query(Aula).all()

@app.post("/aulaNumber", response_model=AulaOut)
def get_aula_by_number(aula_data: AulaIn, db: Session = Depends(get_db)):
    aula = db.query(Aula).filter(Aula.numero == aula_data.numero).first()
    if not aula:
        raise HTTPException(status_code=404, detail="Aula no trobada")
    return aula

@app.post("/aulaInsert", response_model=AulaOut)
def insert_aula(aula_data: AulaIn, db: Session = Depends(get_db)):
    if db.query(Aula).filter_by(numero=aula_data.numero).first():
        raise HTTPException(status_code=400, detail="Aula ja existeix")

    nova_aula = Aula(**aula_data.model_dump())
    db.add(nova_aula)
    db.commit()
    db.refresh(nova_aula)

    return nova_aula

#-----------------------------ENDPOINTS PER ELS GRUPS--------------------------------------------------------

@app.get("/grups", response_model=List[GrupOut])
def get_all_grups(db: Session = Depends(get_db)):
    return db.query(Grup).all()

@app.post("/grupId", response_model=GrupOut)
def get_grup_by_id(grup_data: GrupIn, db: Session = Depends(get_db)):
    grup = db.query(Grup).filter(Grup.id == grup_data.id).first()
    if not grup:
        raise HTTPException(status_code=404, detail="Grup no trobat")
    return grup

@app.post("/grupInsert", response_model=GrupOut)
def insert_grup(grup_data: GrupIn, db: Session = Depends(get_db)):

    nou_grup = Grup(**grup_data.model_dump())
    db.add(nou_grup)
    db.commit()
    db.refresh(nou_grup)

    return nou_grup

@app.post("/grupUpdate/{grup_id}", response_model=GrupOut)
def update_grup(grup_id: int, grup_data: GrupUpdate, db: Session = Depends(get_db)):
    grup = db.query(Grup).filter(Grup.id == grup_id).first()
    if not grup:
        raise HTTPException(status_code=404, detail="Grup no trobat")

    for key, value in grup_data.model_dump(exclude_unset=True).items():
        setattr(grup, key, value)

    db.commit()
    db.refresh(grup)

    return grup

@app.post("/grupDelete/{grup_id}")
def delete_grup(grup_id: int, db: Session = Depends(get_db)):
    grup = db.query(Grup).filter(Grup.id == grup_id).first()
    if not grup:
        raise HTTPException(status_code=404, detail="Grup no trobat")

    db.delete(grup)
    db.commit()

    return {"detail": "Grup eliminat correctament"}

#-----------------------------ENDPOINTS PER ELS CURSOS--------------------------------------------------------
@app.get("/cursos", response_model=List[CursOut])
def get_all_cursos(db: Session = Depends(get_db)):
    return db.query(Curs).all()

@app.post("/cursCode", response_model=CursOut)
def get_curs_by_code(curs_data: CursIn, db: Session = Depends(get_db)):
    curs = db.query(Curs).filter(Curs.codi == curs_data.codi).first()
    if not curs:
        raise HTTPException(status_code=404, detail="Curs no trobat")
    return curs

@app.post("/cursInsert", response_model=CursOut)
def insert_curs(curs_data: CursIn, db: Session = Depends(get_db)):
    if db.query(Curs).filter_by(codi=curs_data.codi).first():
        raise HTTPException(status_code=400, detail="Curs ja existeix")

    nou_curs = Curs(**curs_data.model_dump())
    db.add(nou_curs)
    db.commit()
    db.refresh(nou_curs)

    return nou_curs



#-----------------------------ENDPOINTS PER LES MATRÍCULES--------------------------------------------------------

@app.get("/matricules", response_model=List[MatriculaOut])
def get_all_matricules(db: Session = Depends(get_db)):
    return db.query(Matricula).all()

@app.post("/matriculaInsert", response_model=MatriculaOut)
def insert_matricula(matricula_data: MatriculaIn, db: Session = Depends(get_db)):
    if db.query(Matricula).filter_by(alumne_user=matricula_data.alumne_user, grup_id=matricula_data.grup_id).first():
        raise HTTPException(status_code=400, detail="Matricula ja existeix per aquest alumne i grup")

    nova_matricula = Matricula(**matricula_data.model_dump())
    db.add(nova_matricula)
    db.commit()
    db.refresh(nova_matricula)

    return nova_matricula

@app.post("/matriculaUpdate/{alumne_user}/{grup_id}", response_model=MatriculaOut)
def update_matricula(alumne_user: str, grup_id: int, matricula_data: MatriculaUpdate, db: Session = Depends(get_db)):
    matricula = db.query(Matricula).filter(Matricula.alumne_user == alumne_user, Matricula.grup_id == grup_id).first()
    if not matricula:
        raise HTTPException(status_code=404, detail="Matricula no trobada")

    for key, value in matricula_data.model_dump(exclude_unset=True).items():
        setattr(matricula, key, value)

    db.commit()
    db.refresh(matricula)

    return matricula

@app.post("/matriculaGrup", response_model=List[MatriculaOut])
def get_matricula_by_grup(grup_id: int, db: Session = Depends(get_db)):
    matricula = db.query(Matricula).filter(Matricula.grup_id == grup_id).all()
    if not matricula:
        raise HTTPException(status_code=404, detail="Matricula no trobada")
    return matricula

@app.post("/martriculaDelete/{alumne_user}/{grup_id}")
def delete_matricula(alumne_user: str, grup_id: int, db: Session = Depends(get_db)):
    matricula = db.query(Matricula).filter(Matricula.alumne_user == alumne_user, Matricula.grup_id == grup_id).first()
    if not matricula:
        raise HTTPException(status_code=404, detail="Matricula no trobada")

    db.delete(matricula)
    db.commit()

    return {"detail": "Matricula eliminada correctament"}