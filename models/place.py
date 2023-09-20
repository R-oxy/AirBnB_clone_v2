#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from models.city import City
from models.user import User
from os import getenv


class Place(BaseModel, Base):
    """ A place to stay """
    if getenv("HBNB_TYPE_STORAGE") == "db":
        __tablename__ = 'places'
        city_id = Column(String(60), ForeignKey(City.id), nullable=False)
        user_id = Column(String(60), ForeignKey(User.id), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        place_amenities = relationship("Amenity", secondary="place_amenity",back_populates="place_amenities", viewonly=False)
        amenity_ids = []
        reviews = relationship("Review", backref="place", cascade="all, delete-orphan")
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            """Getter attribute in case of file storage"""
            all_reviews = models.storage.all(Review)
            place_reviews = []
            for review in all_reviews.values():
                if review.place_id == self.id:
                    place_reviews.append(review)
            return place_reviews

        @property
        def amenities(self):
            """ Getter attribute for amenities in FileStorage """
            from models import storage
            amenity_ids = self.amenity_ids
            amenities = []
            for amenity_id in amenity_ids:
                amenity = storage.get(Amenity, amenity_id)
                if amenity:
                    amenities.append(amenity)
            return amenities

        @amenities.setter
        def amenities(self, obj):
            """ Setter attribute for amenities in FileStorage """
            if isinstance(obj, Amenity):
                if obj.id not in self.amenity_ids:
                    self.amenity_ids.append(obj.id)
