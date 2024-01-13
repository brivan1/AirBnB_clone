#!/usr/bin/python3
from uuid import uuid4
from datetime import datetime
import models


class BaseModel:
    """defines all common attributes/methods for other classes"""
    def __init__(self, *args, **kwargs):
        """
        *args, **kwargs arguments for the constructor of a BaseModel
        *args wont be used
        """
        fmt = "%Y-%m-%dT%H:%M:%S.%f"
        self.id = str(uuid4())
        self.created_at = datetime.today()
        self.updated_at = datetime.today()
        """checks if kwargs is not empty then convert the value of the key
        in the dict to fmt format
        """
        if len(kwargs) != 0:
            for k, v in kwargs.items():
                if k == "created_at" or k == "updated_at":
                    self.__dict__[k] = datetime.strptime(v, fmt)
                else:
                    self.__dict__[k] = v
        else:
            models.storage.new(self)

    def __str__(self):
        """converts the instance to a string"""
        className = self.__class__.__name__
        return f" [{className}] ({self.id}) {self.__dict__}"

    def save(self):
        """updates public instance att updated_at with the curr date"""
        self.updated_at = datetime.today()
        models.storage.save()

    def to_dict(self):
        """returns a dict with all keys of __dict__ of the instance"""
        dcopy = self.__dict__.copy()
        dcopy["__class__"] = self.__class__.__name__
        dcopy["created_at"] = self.created_at.isoformat()
        dcopy["updated_at"] = self.updated_at.isoformat()
        return dcopy
