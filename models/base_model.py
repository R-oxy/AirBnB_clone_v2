#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
from uuid import uuid4
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import models

Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models."""

    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, *args, **kwargs):
        """Instantiates a new model."""
        if not kwargs:
            self.id = str(uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()
        else:
            if 'created_at' in kwargs:
                kwargs['created_at'] = datetime.strptime
                (kwargs['created_at'], '%Y-%m-%dT%H:%M:%S.%f')
            if 'updated_at' in kwargs:
                kwargs['updated_at'] = datetime.strptime
                (kwargs['updated_at'], '%Y-%m-%dT%H:%M:%S.%f')
            if '__class__' in kwargs:
                del kwargs['__class__']
            self.__dict__.update(kwargs)

    def __str__(self):
        """Returns a string representation of the instance."""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """
        Updates updated_at with the current time
        when the instance is changed.
        """
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Convert instance into dict format."""
        dictionary = self.__dict__.copy()
        if '_sa_instance_state' in dictionary:
            del dictionary['_sa_instance_state']
        dictionary.update({'__class__': (str(type(self))
                                         .split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        return dictionary

    def delete(self):
        """Deletes the current instance from the storage."""
        models.storage.delete(self)
