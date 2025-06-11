from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from models.trainer import Trainer
from schemas.trainer import TrainerOut, TrainerIn
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

@app.get("/trainers", response_model=List[TrainerOut])
def get_all_trainers(db: Session = Depends(get_db)):
    return db.query(Trainer).all()

@app.post("/trainerName", response_model=TrainerOut)
def get_all_trainers(siome: TrainerIn, db: Session = Depends(get_db)):
    
    return  db.query(Trainer).filter(Trainer.usuari == siome.usuari).first()