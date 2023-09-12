import datetime
from sqlalchemy import Column, Integer, String, DateTime, func, TypeDecorator
from sqlalchemy.ext.mutable import MutableList

from .database import Base

class Person(Base):
    __tablename__ = "persons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    createdAt = Column(String)
    updatedAt = Column(String)

    def __getitem__(self, field):
        return self.__dict__[field]