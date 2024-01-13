#!/usr/bin/python3
import json
import os


class FileStorage:
    __file_path = "file.json"
    __object = {}

    def all(self):

        return FileStorage.__object

    def new(self, obj):

        """method related to managing a storage mechanism
           key: created the key of the instance
        """
        key = f"{type(obj).__name__} {obj.id}"
        """using the key in __object and setting the value to obj"""
        FileStorage.__object[key] = obj

    def save(self):

        """ serializes __objects to the JSON file """
        with open(FileStorage.__file_path, "w", encoding="utf-8") as f:
            d = {k: v.to_dict() for k, v in FileStorage.__object.items()}
            json.dump(d, f)

    def clses(self):
        """Returns a dict of valid classes and reference"""
        from models.base_model import BaseModel
        from models.state import State
        from models.user import User
        from models.place import Place
        from models.amenity import Amenity
        from models.city import City
        from models.review import Review

        clses = {"BaseModel": BaseModel,
                 "User": User,
                 "State": State,
                 "City": City,
                 "Amenity": Amenity,
                 "Place": Place,
                 "Review": Review}
        return clses

    def reload(self):

        """deserializes the JSON file to __objects only if it's a JSON file
           otherwise do nothing,no execption to be raised"""
        if not os.path.isfile(FileStorage.__file_path):
            return
        with open(FileStorage.__file_path, "r", encoding="utf-8") as f:
            obj_d = json.load(f)
            obj_d = {k: self.clses()[v["__class__"]](**v)
                     for k, v in obj_d.items()}

    def attributes(self):
        """Returns attributes and types for className"""
        attributes = {
            "BaseModel":
                     {"id": str,
                      "created_at": datetime.datetime,
                      "updated_at": datetime.datetime},
            "User":
                     {"email": str,
                      "password": str,
                      "first_name": str,
                      "last_name": str},
            "State":
                     {"name": str},
            "City":
                     {"state_id": str,
                      "name": str},
            "Amenity":
                     {"name": str},
            "Place":
                     {"city_id": str,
                      "user_id": str,
                      "name": str,
                      "description": str,
                      "number_rooms": int,
                      "number_bathrooms": int,
                      "max_guest": int,
                      "price_by_night": int,
                      "latitude": float,
                      "longitude": float,
                      "amenity_ids": list},
            "Review":
            {"place_id": str,
                         "user_id": str,
                         "text": str}
        }
