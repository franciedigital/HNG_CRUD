from typing import List
import requests
from fastapi import Depends, FastAPI, HTTPException, Query
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
    return {"message": "Welcome to Francie hng stage two"}


@app.post("/api", response_model=schemas.Person)
async def create_user(person: schemas.PersonCreate, db: Session = Depends(get_db)):
    # Convert the name to lowercase
    person.name = person.name.lower()

    # Check if a user with the same lowercase name already exists
    db_person = personInstance.get_user_by_name(name=person.name, db=db)
    if db_person:
        raise HTTPException(status_code=409, detail="User already exists")

    # Create the user with the lowercase name
    new_person = person
    db_person = personInstance.create_user(db=db, person=new_person)

    return db_person


@app.get("/api/user_id")
async def get_user(name: str = Query(..., description="Name of the user"), db: Session = Depends(get_db)):
    if not name:
        raise HTTPException(
            status_code=400, detail="Name query parameter is required")

    name = name.lower()

    db_person = personInstance.get_user_by_name(name=name, db=db)

    if db_person is None:
        raise HTTPException(
            status_code=404, detail=f"User with name '{name}' not found")

    return db_person


@app.delete("/api/user_id")
def delete_user(name: str = Query(..., description="Name of the user"), db: Session = Depends(get_db)):
    name = name.lower()
    db_person = personInstance.get_user_by_name(name=name, db=db)

    if db_person is None:
        raise HTTPException(status_code=404, detail="User not found")
    deleted_user = personInstance.delete_user_by_name(name=name, db=db)
    if deleted_user:
        return {"message": f"User with name {name} has been deleted"}
    raise HTTPException(status_code=500, detail="Failed to delete user")


@app.put("/api/user_id", response_model=schemas.Person)
def update_user(person: schemas.PersonCreate, name: str = Query(..., description="Name of the user to update"), db: Session = Depends(get_db)):
    person.name = person.name.lower()
    name = name.lower()

    db_person = personInstance.get_user_by_name(name=name, db=db)
    if db_person is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    updated_user = personInstance.update_user_by_name(name=name, new_name=person.name, db=db)
    if not updated_user:
        raise HTTPException(status_code=500, detail="Failed to update user")
    return updated_user
