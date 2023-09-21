#!/usr/bin/python3
"""DB storage class for AirBnB"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import BaseModel, Base
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from os import getenv


class DBStorage:
    """DBStorage class"""

    __engine = None
    __session = None

    def __init__(self):
        """Constructor for DBStorage"""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}:3306/{}'
                                      .format(getenv('HBNB_MYSQL_USER'),
                                              getenv('HBNB_MYSQL_PWD'),
                                              getenv('HBNB_MYSQL_HOST'),
                                              getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ Query on the current database session (self.__session) """

        # If cls is None, query all types of objects
        if cls is None:
            objs = self.__session.query(User).all()
            objs.extend(self.__session.query(State).all())
            objs.extend(self.__session.query(City).all())
            objs.extend(self.__session.query(Place).all())
            objs.extend(self.__session.query(Review).all())
            objs.extend(self.__session.query(Amenity).all())

        # If cls is specified, query objects of that class
        else:
            if type(cls) == str:
                cls = eval(cls)
            objs = self.__session.query(cls)

        # Create a dictionary of objects
        obj_dict = {}
        for obj in objs:
            key = type(obj).__name__ + "." + obj.id
            obj_dict[key] = obj

        return obj_dict

    def new(self, obj):
        """Add object to current database session"""
        if obj:
            self.__session.add(obj)

    def save(self):
        """Commit all changes to current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete object from current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database and create current session"""
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(sessionmaker(bind=self.__engine,
                                                     expire_on_commit=False))

    def close(self):
        """Close the current session"""
        self.__session.close()
