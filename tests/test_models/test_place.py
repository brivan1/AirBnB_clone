#!/usr/bin/python3

import os
import models
import unittest
from models.place import Place
from datetime import datetime
from time import sleep

"""Defines unit tests for place.py.
Unittest classes:
    TestPlace_instantiation
    TestPlace_save
    TestPlace_to_dict
"""


class Test_PlaceInstin(unittest.TestCase):
    """Unit tests for testing instantiation"""

    def test_noArgs(self):
        self.assertEqual(Place, type(Place()))

    def test_newInstanceInObj(self):
        self.assertIn(Place(), models.storage.all().values())

    def test_idPublicStr(self):
        self.assertEqual(str, type(Place().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Place().created_at))

    def test_updated_atPublic_datetime(self):
        self.assertEqual(datetime, type(Place().updated_at))

    def test_cityIdPublicClassAttr(self):
        pla = Place()
        self.assertEqual(str, type(Place.city_id))
        self.assertIn("city_id", dir(pla))
        self.assertNotIn("city_id", pla.__dict__)

    def test_UseridPublicClassAttr(self):
        pla = Place()
        self.assertEqual(str, type(Place.user_id))
        self.assertIn("user_id", dir(pla))
        self.assertNotIn("user_id", pla.__dict__)

    def test_namepublicClassAttr(self):
        pla = Place()
        self.assertEqual(str, type(Place.name))
        self.assertIn("name", dir(pla))
        self.assertNotIn("name", pla.__dict__)

    def test_descriPublicClassAttr(self):
        pla = Place()
        self.assertEqual(str, type(Place.description))
        self.assertIn("description", dir(pla))
        self.assertNotIn("desctiption", pla.__dict__)

    def test_number_rooms_is_public_class_attribute(self):
        pl = Place()
        self.assertEqual(int, type(Place.number_rooms))
        self.assertIn("number_rooms", dir(pl))
        self.assertNotIn("number_rooms", pl.__dict__)

    def test_numbathroomsIsPublicClassAttr(self):
        pla = Place()
        self.assertEqual(int, type(Place.number_bathrooms))
        self.assertIn("number_bathrooms", dir(pla))
        self.assertNotIn("number_bathrooms", pla.__dict__)

    def test_maxGuestPublicClassAttr(self):
        pla = Place()
        self.assertEqual(int, type(Place.max_guest))
        self.assertIn("max_guest", dir(pla))
        self.assertNotIn("max_guest", pla.__dict__)

    def test_priceAtNightPublicClassAttr(self):
        pla = Place()
        self.assertEqual(int, type(Place.price_by_night))
        self.assertIn("price_by_night", dir(pla))
        self.assertNotIn("price_by_night", pla.__dict__)

    def test_latitudeIsPublicClassAttri(self):
        pla = Place()
        self.assertEqual(float, type(Place.latitude))
        self.assertIn("latitude", dir(pla))
        self.assertNotIn("latitude", pla.__dict__)

    def test_longitudePublicClassAttr(self):
        pla = Place()
        self.assertEqual(float, type(Place.longitude))
        self.assertIn("longitude", dir(pla))
        self.assertNotIn("longitude", pla.__dict__)

    def test_amenityIdsPublicClassAttri(self):
        pla = Place()
        self.assertEqual(list, type(Place.amenity_ids))
        self.assertIn("amenity_ids", dir(pla))
        self.assertNotIn("amenity_ids", pla.__dict__)

    def test_twoPlacesUniqueIds(self):
        pla1 = Place()
        pla2 = Place()
        self.assertNotEqual(pla1.id, pla2.id)

    def test_twoPlacesDiffCreated_at(self):
        pla1 = Place()
        sleep(0.05)
        pla2 = Place()
        self.assertLess(pla1.created_at, pla2.created_at)

    def test_twoPlacesDiffupdated_at(self):
        pla1 = Place()
        sleep(0.05)
        pla2 = Place()
        self.assertLess(pla1.updated_at, pla2.updated_at)

    def test_strRepre(self):
        dates = datetime.today()
        dates_repr = repr(dates)
        pla = Place()
        pla.id = "124680"
        pla.created_at = pla.updated_at = dates
        plastr = pla.__str__()
        self.assertIn("[Place] (124680)", plastr)
        self.assertIn("'id': '124680'", plastr)
        self.assertIn("'created_at': " + dates_repr, plastr)
        self.assertIn("'updated_at': " + dates_repr, plastr)

    def test_unusedArgs(self):
        pla = Place(None)
        self.assertNotIn(None, pla.__dict__.values())

    def test_instinWthKwargs(self):
        dates = datetime.today()
        diso = dates.isoformat()
        pla = Place(id="155", created_at=diso, updated_at=diso)
        self.assertEqual(pla.id, "155")
        self.assertEqual(pla.created_at, dates)
        self.assertEqual(pla.updated_at, dates)

    def test_instinWthnkwargs(self):
        with self.assertRaises(TypeError):
            Place(id=None, created_at=None, updated_at=None)


class Test_PlaceSave(unittest.TestCase):
    """Unit tests for testing save() of the Place class"""

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
        pla = Place()
        sleep(0.05)
        first_updated_at = pla.updated_at
        pla.save()
        self.assertLess(first_updated_at, pla.updated_at)

    def test_twoSaves(self):
        pla = Place()
        sleep(0.05)
        first_updated_at = pla.updated_at
        pla.save()
        sec_updated_at = pla.updated_at
        self.assertLess(first_updated_at, sec_updated_at)
        sleep(0.05)
        pla.save()
        self.assertLess(sec_updated_at, pla.updated_at)

    def test_saveWthArg(self):
        pla = Place()
        with self.assertRaises(TypeError):
            pla.save(None)

    def test_saveUpdates_file(self):
        pla = Place()
        pla.save()
        plid = "Place." + pla.id
        with open("file.json", "r") as f:
            self.assertIn(plid, f.read())


class TestPlace_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the Place class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(Place().to_dict()))

    def test_toDictDatetimeAttriStrs(self):
        pl = Place()
        pl_dict = pl.to_dict()
        self.assertEqual(str, type(pl_dict["id"]))
        self.assertEqual(str, type(pl_dict["created_at"]))
        self.assertEqual(str, type(pl_dict["updated_at"]))

    def test_toDictontainsCorrectKeys(self):
        pl = Place()
        self.assertIn("id", pl.to_dict())
        self.assertIn("created_at", pl.to_dict())
        self.assertIn("updated_at", pl.to_dict())
        self.assertIn("__class__", pl.to_dict())

    def test_toDictContainsAddedAttr(self):
        pla = Place()
        pla.middle_name = "soma"
        pla.my_number = 50
        self.assertEqual("soma", pla.middle_name)
        self.assertIn("my_number", pla.to_dict())

    def test_ToDictOutput(self):
        dates = datetime.today()
        pla = Place()
        pla.id = "123456"
        pla.created_at = pla.updated_at = dates
        todict = {
            'id': '123456',
            '__class__': 'Place',
            'created_at': dates.isoformat(),
            'updated_at': dates.isoformat(),
        }
        self.assertDictEqual(pla.to_dict(), todict)

    def test_contrastToDictDunderDict(self):
        pla = Place()
        self.assertNotEqual(pla.to_dict(), pla.__dict__)

    def test_toDictWthArg(self):
        pla = Place()
        with self.assertRaises(TypeError):
            pla.to_dict(None)


if __name__ == "__main__":
    unittest.main()
