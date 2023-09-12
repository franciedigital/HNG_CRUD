from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import logging

from . import models, schemas

class Person:
    def create_user(self, db: Session, person: schemas.Person):
        psn = {}
        t_time = datetime.now()

        psn['createdAt'] = t_time.strftime('%Y-%m-%d %H:%M:%S.%f')
        psn['updatedAt'] = t_time.strftime('%Y-%m-%d %H:%M:%S.%f')

        db_person = models.Person(name=person.name,createdAt=psn['createdAt'],updatedAt=psn['updatedAt'])

        db.add(db_person)

        try:
            db.commit()
            db.refresh(db_person)

            return db_person
        except SQLAlchemyError as e:
            db.rollback()
            logging.error(
                "Failed to Commit because of {error}. Doing Rollback".format(error=e))
            
    
    def get_user_by_name(self, name: str, db: Session):
        return db.query(models.Person).filter(models.Person.name == name).first()

    
    def delete_user_by_name(self, name: str, db: Session):
        user = db.query(models.Person).filter(models.Person.name == name).first()
    
        if user:
            # If the user exists, delete them from the database
            db.delete(user)
            db.commit()
            return True 
        else:
            return False  # Indicate that the user was not found
        
    def update_user_by_name(self, name: str, new_name: str, db: Session):
        # Find the user with the current name
        user = db.query(models.Person).filter(models.Person.name == name).first()

        if user:
            # Update the user's name with the new name
            user.name = new_name
            user.updatedAt = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

            # Commit the changes to the database
            db.commit()
            db.refresh(user)

            return user
        else:
            # Indicate that the user was not found
            return None




        