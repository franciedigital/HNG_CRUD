from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
import logging
import random
import time
import json

from . import models, schemas

class Person:
    def create_person(self, db: Session, person: schemas.Person):
        psn = {}
        t_time = datetime.now()

        psn['createdAt'] = t_time.strftime('%Y-%m-%d %H:%M:%S.%f')
        psn['updatedAt'] = t_time.strftime('%Y-%m-%d %H:%M:%S.%f')

        db_person = models.Person(fullname=person.fullname,createdAt=psn['createdAt'],updatedAt=psn['updatedAt'])

        db.add(db_person)

        try:
            db.commit()
            db.refresh(db_person)

            return db_person
        except SQLAlchemyError as e:
            db.rollback()
            logging.error(
                "Failed to Commit because of {error}. Doing Rollback".format(error=e))
            
    
    def get_user_by_id(self, user_id: int, db: Session):
        return db.query(models.Person).filter(models.Person.id==user_id).first()
    
    def delete_user_by_id(self, user_id: int, db: Session):
        user = db.query(models.Person).filter(models.Person.id == user_id).first()
    
        if user:
            # If the user exists, delete them from the database
            db.delete(user)
            db.commit()
            return True 
        else:
            return False  # Indicate that the user was not found



        