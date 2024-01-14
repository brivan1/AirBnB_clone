#!/usr/bin/python3
import os
import models
from time import sleep
from datetime import datetime
from models.city import City
import unittest

"""Defines unit tests for city.py.
Unit test classes:
    TestCity_instantiation
    TestCity_save
    TestCity_to_dict
"""


class TestCity_instin(unittest.TestCase):
    """Unit tests for testing instin of the City class"""

    def test_noArgsInstin(self):
        self.assertEqual(City, type(City()))

    def test_newInstanceStoredInObj(self):
        self.assertIn(City(), models.storage.all().values())

    def test_idIsPublic_str(self):
        self.assertEqual(str, type(City().id))

    def test_createdAtIsPublicDatetime(self):
        self.assertEqual(datetime, type(City().created_at))

    def test_updated_at_isPublicDatetime(self):
        self.assertEqual(datetime, type(City().updated_at))

    def test_stateIdIsPublicClassAttr(self):
        cty = City()
        self.assertEqual(str, type(City.state_id))
        self.assertIn("state_id", dir(cty))
        self.assertNotIn("state_id", cty.__dict__)

    def test_nameIsPublicClassAttr(self):
        cty = City()
        self.assertEqual(str, type(City.name))
        self.assertIn("name", dir(cty))
        self.assertNotIn("name", cty.__dict__)

    def test_two_cities_unique_ids(self):
        cty1 = City()
        cty2 = City()
        self.assertNotEqual(cty1.id, cty2.id)

    def test_twoCitiesDiffCreated_at(self):
        cty1 = City()
        sleep(0.05)
        cty2 = City()
        self.assertLess(cty1.created_at, cty2.created_at)

    def test_twoCitiesDiffupdated_at(self):
        cty1 = City()
        sleep(0.05)
        cty2 = City()
        self.assertLess(cty1.updated_at, cty2.updated_at)

    def test_strRepre(self):
        dates = datetime.today()
        dates_repr = repr(dates)
        cty = City()
        cty.id = "246801"
        cty.created_at = cty.updated_at = dates
        ctystr = cty.__str__()
        self.assertIn("[City] (246801)", ctystr)
        self.assertIn("'id': '246801'", ctystr)
        self.assertIn("'created_at': " + dates_repr, ctystr)
        self.assertIn("'updated_at': " + dates_repr, ctystr)

    def test_unusedAargs(self):
        cty = City(None)
        self.assertNotIn(None, cty.__dict__.values())

    def test_instinWthKwargs(self):
        dates = datetime.today()
        diso = dates.isoformat()
        cty = City(id="155", created_at=diso, updated_at=diso)
        self.assertEqual(cty.id, "155")
        self.assertEqual(cty.created_at, dates)
        self.assertEqual(cty.updated_at, dates)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            City(id=None, created_at=None, updated_at=None)


class Test_CitySave(unittest.TestCase):
    """Unit tests for testing save method of the City class."""

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
        cty = City()
        sleep(0.05)
        first_updated_at = cty.updated_at
        cty.save()
        self.assertLess(first_updated_at, cty.updated_at)

    def test_twoSaves(self):
        cty = City()
        sleep(0.05)
        first_updated_at = cty.updated_at
        cty.save()
        second_updated_at = cty.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        cty.save()
        self.assertLess(second_updated_at, cty.updated_at)

    def test_SaveWthArg(self):
        cty = City()
        with self.assertRaises(TypeError):
            cty.save(None)

    def test_saveUpdates_file(self):
        cty = City()
        cty.save()
        ctyid = "City." + cty.id
        with open("file.json", "r") as f:
            self.assertIn(ctyid, f.read())


class Test_CityToDict(unittest.TestCase):
    """Unit tests for testing to_dict method of the City class"""

    def test_toDictType(self):
        self.assertTrue(dict, type(City().to_dict()))

    def test_toDictContainsCorrectKeys(self):
        cty = City()
        self.assertIn("id", cty.to_dict())
        self.assertIn("created_at", cty.to_dict())
        self.assertIn("updated_at", cty.to_dict())
        self.assertIn("__class__", cty.to_dict())

    def test_toDictContainsAddedAttr(self):
        cty = City()
        cty.middle_name = "soma"
        cty.my_number = 50
        self.assertEqual("soma", cty.middle_name)
        self.assertIn("my_number", cty.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        cty = City()
        cty_dict = cty.to_dict()
        self.assertEqual(str, type(cty_dict["id"]))
        self.assertEqual(str, type(cty_dict["created_at"]))
        self.assertEqual(str, type(cty_dict["updated_at"]))

    def test_to_dict_output(self):
        dates = datetime.today()
        cty = City()
        cty.id = "246801"
        cty.created_at = cty.updated_at = dates
        todict = {
            'id': '246801',
            '__class__': 'City',
            'created_at': dates.isoformat(),
            'updated_at': dates.isoformat(),
        }
        self.assertDictEqual(cty.to_dict(), todict)

    def test_contrastToDictDunderDict(self):
        cty = City()
        self.assertNotEqual(cty.to_dict(), cty.__dict__)

    def test_toDictwthArg(self):
        cty = City()
        with self.assertRaises(TypeError):
            cty.to_dict(None)


if __name__ == "__main__":
    unittest.main()
