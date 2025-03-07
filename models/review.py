#!/usr/bin/python3
""" Review module for the HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from models.place import Place
from models.user import User
from os import getenv


class Review(BaseModel, Base):
    """ Review class to store review information """

    __tablename__ = 'reviews'

    if getenv("HBNB_TYPE_STORAGE") == "db":
        text = Column(String(1024), nullable=False)
        place_id = Column(String(60, collation='latin1_swedish_ci'), ForeignKey('places.id'), nullable=False)
        user_id = Column(String(60, collation='latin1_swedish_ci'), ForeignKey('users.id'), nullable=False)
