#!/usr/bin/python3
"""Defines unit tests for models/engine/file_storage.py

Unit test classes:
    TestFileStorage_instantiation
    TestFileStorage_methods
"""
import os
import json
import models
import unittest
from models.review import Review
from datetime import datetime
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.place import Place
from models.city import City
from models.engine.file_storage import FileStorage
from models.amenity import Amenity


class TestFileStorage_instin(unittest.TestCase):
    """Unit tests for testing instantiation of the FileStorage class"""

    def test_FileStorageInstinNoArgs(self):
        self.assertEqual(type(FileStorage()), FileStorage)

    def test_FileStorageInstINWthArg(self):
        with self.assertRaises(TypeError):
            FileStorage(None)

    def test_FileStorageFilePathIsPrvtStr(self):
        self.assertEqual(str, type(FileStorage._FileStorage__file_path))

    def testFileStorage_objIsPrivateDict(self):
        self.assertEqual(dict, type(FileStorage._FileStorage__objects))

    def test_storageInitializes(self):
        self.assertEqual(type(models.storage), FileStorage)


class TestFileStorage_mthods(unittest.TestCase):
    """Unit tests for testing methods of the FileStorage class"""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}

    def test_all(self):
        self.assertEqual(dict, type(models.storage.all()))

    def test_allWthArg(self):
        with self.assertRaises(TypeError):
            models.storage.all(None)

    def testNew(self):
        uid = BaseModel()
        use = User()
        sta = State()
        pla = Place()
        cty = City()
        ame = Amenity()
        rv = Review()
        models.storage.new(uid)
        models.storage.new(use)
        models.storage.new(sta)
        models.storage.new(pla)
        models.storage.new(cty)
        models.storage.new(ame)
        models.storage.new(rv)
        self.assertIn("BaseModel." + uid.id, models.storage.all().keys())
        self.assertIn(uid, models.storage.all().values())
        self.assertIn("User." + use.id, models.storage.all().keys())
        self.assertIn(use, models.storage.all().values())
        self.assertIn("State." + sta.id, models.storage.all().keys())
        self.assertIn(sta, models.storage.all().values())
        self.assertIn("Place." + pla.id, models.storage.all().keys())
        self.assertIn(pla, models.storage.all().values())
        self.assertIn("City." + cty.id, models.storage.all().keys())
        self.assertIn(cty, models.storage.all().values())
        self.assertIn("Amenity." + ame.id, models.storage.all().keys())
        self.assertIn(ame, models.storage.all().values())
        self.assertIn("Review." + rv.id, models.storage.all().keys())
        self.assertIn(rv, models.storage.all().values())

    def test_newWthArgs(self):
        with self.assertRaises(TypeError):
            models.storage.new(BaseModel(), 1)

    def test_save(self):
        uid = BaseModel()
        use = User()
        sta = State()
        pla = Place()
        cty = City()
        ame = Amenity()
        rv = Review()
        models.storage.new(uid)
        models.storage.new(use)
        models.storage.new(sta)
        models.storage.new(pla)
        models.storage.new(cty)
        models.storage.new(ame)
        models.storage.new(rv)
        models.storage.save()
        save_txt = ""
        with open("file.json", "r") as f:
            save_text = f.read()
            self.assertIn("BaseModel." + uid.id, save_text)
            self.assertIn("User." + use.id, save_text)
            self.assertIn("State." + sta.id, save_text)
            self.assertIn("Place." + pla.id, save_text)
            self.assertIn("City." + cty.id, save_text)
            self.assertIn("Amenity." + ame.id, save_text)
            self.assertIn("Review." + rv.id, save_text)

    def test_saveWthArg(self):
        with self.assertRaises(TypeError):
            models.storage.save(None)

    def test_reload(self):
        uid = BaseModel()
        use = User()
        sta = State()
        pla = Place()
        cty = City()
        ame = Amenity()
        rv = Review()
        models.storage.new(uid)
        models.storage.new(use)
        models.storage.new(sta)
        models.storage.new(pla)
        models.storage.new(cty)
        models.storage.new(ame)
        models.storage.new(rv)
        models.storage.save()
        models.storage.reload()
        objs = FileStorage._FileStorage__objects
        self.assertIn("BaseModel." + uid.id, objs)
        self.assertIn("User." + use.id, objs)
        self.assertIn("State." + sta.id, objs)
        self.assertIn("Place." + pla.id, objs)
        self.assertIn("City." + cty.id, objs)
        self.assertIn("Amenity." + ame.id, objs)
        self.assertIn("Review." + rv.id, objs)

    def test_reload_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.reload(None)


if __name__ == "__main__":
    unittest.main()
