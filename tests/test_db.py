import os
import json
import unittest

from infrastructure import db


class DBTestCase(unittest.TestCase):
    def setUp(self):
        if os.path.exists(db.DB_PATH):
            os.remove(db.DB_PATH)

    def test_init_schema(self):
        db.init_schema()
        self.assertTrue(os.path.exists(db.DB_PATH))
        with open(db.DB_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.assertEqual(data['clients'], [])
        self.assertEqual(data['rooms'], [])
        self.assertEqual(data['reservations'], [])
        self.assertEqual(data['auto_id']['client'], 0)
