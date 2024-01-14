#!/usr/bin/python3
import os
import models
import unittest
from time import sleep
from datetime import datetime
from models.amenity import Amenity

"""Defines unit tests for amenity.py
Unit test classes:
    TestAmenity_instantiation
    TestAmenity_save
    TestAmenity_to_dict
"""


class Test_amenityInstin(unittest.TestCase):
    """Unit tests for testing instantiation of the Amenity class"""

    def test_noArgsInstin(self):
        self.assertEqual(Amenity, type(Amenity()))

    def test_newInstanceStoredInObj(self):
        self.assertIn(Amenity(), models.storage.all().values())

    def test_idIsPublicStr(self):
        self.assertEqual(str, type(Amenity().id))

    def test_createdAtIsPublicDatetime(self):
        self.assertEqual(datetime, type(Amenity().created_at))

    def test_updated_atIsPublicDatetime(self):
        self.assertEqual(datetime, type(Amenity().updated_at))

    def test_nameIsPublicClassAttr(self):
        ame = Amenity()
        self.assertEqual(str, type(Amenity.name))
        self.assertIn("name", dir(Amenity()))
        self.assertNotIn("name", ame.__dict__)

    def test_twoAmenitiesUniqueIds(self):
        ame1 = Amenity()
        ame2 = Amenity()
        self.assertNotEqual(ame1.id, ame2.id)

    def test_twoAmenitiesDiffCreated_at(self):
        ame1 = Amenity()
        sleep(0.05)
        ame2 = Amenity()
        self.assertLess(ame1.created_at, ame2.created_at)

    def test_twoAmenitiesDiff_updated_at(self):
        ame1 = Amenity()
        sleep(0.05)
        ame2 = Amenity()
        self.assertLess(ame1.updated_at, ame2.updated_at)

    def test_strRepre(self):
        dates = datetime.today()
        dates_repr = repr(dates)
        ame = Amenity()
        ame.id = "24680"
        ame.created_at = ame.updated_at = dates
        amstr = ame.__str__()
        self.assertIn("[Amenity] (123456)", amstr)
        self.assertIn("'id': '123456'", amstr)
        self.assertIn("'created_at': " + dates_repr, amstr)
        self.assertIn("'updated_at': " + dates_repr, amstr)

    def test_unusedArgs(self):
        ame = Amenity(None)
        self.assertNotIn(None, ame.__dict__.values())

    def test_instinWthKwargs(self):
        """instantiation with kwargs test method"""
        dates = datetime.today()
        diso = dates.isoformat()
        ame = Amenity(id="345", created_at=diso, updated_at=diso)
        self.assertEqual(ame.id, "345")
        self.assertEqual(ame.created_at, dates)
        self.assertEqual(ame.updated_at, dates)

    def test_instinWthNKwargs(self):
        with self.assertRaises(TypeError):
            Amenity(id=None, created_at=None, updated_at=None)


class TestAmenity_save(unittest.TestCase):
    """Unit tests for testing save method of the Amenity class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_oneSave(self):
        ame = Amenity()
        sleep(0.05)
        first_updated_at = ame.updated_at
        ame.save()
        self.assertLess(first_updated_at, ame.updated_at)

    def test_twoSaves(self):
        ame = Amenity()
        sleep(0.05)
        first_updated_at = ame.updated_at
        ame.save()
        second_updated_at = ame.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        ame.save()
        self.assertLess(second_updated_at, ame.updated_at)

    def test_save_updates_file(self):
        ame = Amenity()
        ame.save()
        amid = "Amenity." + ame.id
        with open("file.json", "r") as f:
            self.assertIn(amid, f.read())

    def test_saveWthArg(self):
        ame = Amenity()
        with self.assertRaises(TypeError):
            ame.save(None)


class TestAmenity_toDict(unittest.TestCase):
    """Unit tests for testing to_dict method of the Amenity class."""

    def test_toDictType(self):
        self.assertTrue(dict, type(Amenity().to_dict()))

    def test_toDictContainsCorrectKeys(self):
        ame = Amenity()
        self.assertIn("id", ame.to_dict())
        self.assertIn("created_at", ame.to_dict())
        self.assertIn("updated_at", ame.to_dict())
        self.assertIn("__class__", ame.to_dict())

    def test_toDictContainsAddedAttributes(self):
        ame = Amenity()
        ame.middle_name = "soma"
        ame.my_number = 50
        self.assertEqual("soma", ame.middle_name)
        self.assertIn("my_number", ame.to_dict())

    def test_to_dict_output(self):
        dates = datetime.today()
        ame = Amenity()
        ame.id = "24680"
        ame.created_at = ame.updated_at = dates
        todict = {
            'id': '24680',
            '__class__': 'Amenity',
            'created_at': dates.isoformat(),
            'updated_at': dates.isoformat(),
        }
        self.assertDictEqual(ame.to_dict(), todict)

    def test_to_dict_datetime_attributes_are_strs(self):
        ame = Amenity()
        ame_dict = ame.to_dict()
        self.assertEqual(str, type(ame_dict["id"]))
        self.assertEqual(str, type(ame_dict["created_at"]))
        self.assertEqual(str, type(ame_dict["updated_at"]))

    def test_toDictWthArg(self):
        ame = Amenity()
        with self.assertRaises(TypeError):
            ame.to_dict(None)

    def testContrastToDictDunderDict(self):
        ame = Amenity()
        self.assertNotEqual(ame.to_dict(), ame.__dict__)


if __name__ == "__main__":
    unittest.main()
