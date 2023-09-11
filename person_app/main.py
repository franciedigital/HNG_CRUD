from typing import List
import requests
from fastapi import Depends, FastAPI, HTTPException, Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from . import models, person, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

personInstance = person.Person()


session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def index():
    return {"message": "Welcome to hng stage two"}

@app.post("/api", response_model=schemas.Person)
def create_person(person: schemas.PersonCreate, db: Session = Depends(get_db)):
    new_person = person
    db_person = personInstance.create_person(db=db, person=new_person)

    return db_person

@app.get("/api/{user_id}", response_model=schemas.Person)
def get_person(user_id: int, db: Session = Depends(get_db)):
    db_person = personInstance.get_user_by_id(user_id=user_id, db=db)
    
    if db_person is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_person
    