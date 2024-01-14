#!/usr/bin/python3
import unittest
import os
from time import sleep
import models
from datetime import datetime
from models.base_model import BaseModel

"""
Specifies unit tests for the models/base_model.py module.
Unit test classes include:
TestBaseModel_instantiation
TestBaseModel_save
TestBaseModel_to_dict"
"""


class Test_BaseModelInit(unittest.TestCase):
    """Unit tests for BaseModel initialization."""
    def test_NoArgsInit(self):
        self.assertEqual(BaseModel, type(BaseModel()))

    def test_IdIspublicStr(self):
        self.assertEqual(str, type(BaseModel().id))

    def test_NewInstanceInObj(self):
        self.assertIn(BaseModel(), models.storage.all().values())

    def test_CreatedAtPublic(self):
        self.assertEqual(datetime, type(BaseModel().created_at))

    def test_updatedAtPublic(self):
        self.assertEqual(datetime, type(BaseModel().updated_at))

    def test_modelsUniqueIds(self):
        uid1 = BaseModel()
        uid2 = BaseModel()
        self.assertNotEqual(uid1.id, uid2.id)

    def test_modelsDiffCreatedAt(self):
        uid1 = BaseModel()
        sleep(0.05)
        uid2 = BaseModel()
        self.assertLess(uid1.created_at, uid2.created_at)

    def test_modelsDiffUpdatedAt(self):
        uid1 = BaseModel()
        sleep(0.05)
        uid2 = BaseModel()
        self.assertLess(uid1.updated_at, uid2.updated_at)

    def test_unusedArgs(self):
        uid = BaseModel(None)
        self.assertNotIn(None, uid.__dict__.values())

    def test_instinKwargs(self):
        dates = datetime.today()
        diso = dates.isoformat()
        uid = BaseModel(id="345", created_at=diso, updated_at=diso)
        self.assertEqual(uid.id, "345")
        self.assertEqual(uid.created_at, dates)
        self.assertEqual(uid.updated_at, dates)

    def test_strRepre(self):
        dates = datetime.today()
        datesRepr = repr(dates)
        uid = BaseModel()
        uid.id = "246891"
        uid.created_at = uid.updated_at = dates
        uidstr = uid.__str__()
        self.assertIn("[BaseModel] (246891)", uidstr)
        self.assertIn("'id': '246891'", uidstr)
        self.assertIn("'created_at': " + datesRepr, uidstr)
        self.assertIn("'updated_at': " + datesRepr, uidstr)

    def test_instinNoKwargs(self):
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)

    def test_instinArgsnKwargs(self):
        dates = datetime.today()
        diso = dates.isoformat()
        uid = BaseModel("9", id="155", created_at=diso, updated_at=diso)
        self.assertEqual(uid.id, "155")
        self.assertEqual(uid.created_at, dates)
        self.assertEqual(uid.updated_at, dates)


class Test_BMSave(unittest.TestCase):
    """Unit tests for testing save() of the BaseModel class"""

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

    def test_save(self):
        uid = BaseModel()
        sleep(0.05)
        initial_updated_at = uid.updated_at
        uid.save()
        self.assertLess(initial_updated_at, uid.updated_at)

    def test_twoSaves(self):
        uid = BaseModel()
        sleep(0.05)
        initial_updated_at = uid.updated_at
        uid.save()
        sec_updated_at = uid.updated_at
        self.assertLess(initial_updated_at, sec_updated_at)
        sleep(0.05)
        uid.save()
        self.assertLess(sec_updated_at, uid.updated_at)

    def test_saveUpdatesFile(self):
        uid = BaseModel()
        uid.save()
        uid_id = "BaseModel." + uid.id
        with open("file.json", "r") as f:
            self.assertIn(uid_id, f.read())

    def test_saveWithArg(self):
        uid = BaseModel()
        with self.assertRaises(TypeError):
            uid.save(None)


class Test_BMToDict(unittest.TestCase):
    """Unit tests to test to_dict()"""

    def test_toDictType(self):
        uid = BaseModel()
        self.assertTrue(dict, type(uid.to_dict()))

    def test_toDictWthCorrectKeys(self):
        uid = BaseModel()
        self.assertIn("id", uid.to_dict())
        self.assertIn("created_at", uid.to_dict())
        self.assertIn("updated_at", uid.to_dict())
        self.assertIn("__class__", uid.to_dict())

    def test_toDictWthAttrb(self):
        uid = BaseModel()
        uid.name = "soma"
        uid.my_number = 80
        self.assertIn("name", uid.to_dict())
        self.assertIn("my_number", uid.to_dict())

    def test_toDictAlt(self):
        uid = BaseModel()
        self.assertNotEqual(uid.to_dict(), uid.__dict__)

    def test_toDictArg(self):
        uid = BaseModel()
        with self.assertRaises(TypeError):
            uid.to_dict(None)

    def test_toDictDatetimeStrs(self):
        uid = BaseModel()
        uidDict = uid.to_dict()
        self.assertEqual(str, type(uidDict["created_at"]))
        self.assertEqual(str, type(uidDict["updated_at"]))

    def test_toDictStdout(self):
        dates = datetime.today()
        uid = BaseModel()
        uid.id = "246891"
        uid.created_at = uid.updated_at = dates
        toDict = {
            'id': '246891',
            '__class__': 'BaseModel',
            'created_at': dates.isoformat(),
            'updated_at': dates.isoformat()
        }
        self.assertDictEqual(uid.to_dict(), toDict)


if __name__ == "__main__":
    unittest.main()
