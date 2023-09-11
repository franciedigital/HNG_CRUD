import datetime
from sqlalchemy import Column, Integer, String, DateTime, func, TypeDecorator
from sqlalchemy.ext.mutable import MutableList

from .database import Base


def get_current_timestamp():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

class DatetimeType(TypeDecorator):
    impl = DateTime

    def process_bind_param(self, value, dialect):
        if isinstance(value, datetime.datetime):
            return value.strftime('%Y-%m-%d %H:%M:%S')
        return value

    def process_result_value(self, value, dialect):
        if isinstance(value, str):
            return datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        return value



class Person(Base):
    __tablename__ = "persons"

    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String)
    createdAt = Column(String)
    updatedAt = Column(String)

    def __getitem__(self, field):
        return self.__dict__[field]