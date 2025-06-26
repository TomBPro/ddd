import os
import json
import sys
import subprocess
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
        self.assertEqual(len(data['rooms']), 3)
        self.assertEqual(data['reservations'], [])
        self.assertEqual(data['auto_id']['client'], 0)
        self.assertEqual(data['auto_id']['room'], 3)


class CLITestCase(unittest.TestCase):
    def setUp(self):
        if os.path.exists(db.DB_PATH):
            os.remove(db.DB_PATH)

    def run_cli(self, args):
        result = subprocess.run(
            [sys.executable, 'main.py'] + args,
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()

    def test_cli_init(self):
        output = self.run_cli(['init-db'])
        self.assertIn('Database initialized', output)
        self.assertTrue(os.path.exists(db.DB_PATH))
        with open(db.DB_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.assertEqual(len(data['rooms']), 3)

    def test_cli_add_client(self):
        self.run_cli(['init-db'])
        output = self.run_cli(['add-client', '--name', 'Alice', '--email', 'a@example.com', '--phone', '123'])
        self.assertIn('Client added with id 1', output)
        with open(db.DB_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.assertEqual(len(data['clients']), 1)

    def test_cli_add_room(self):
        self.run_cli(['init-db'])
        output = self.run_cli(['add-room', '--type', 'standard', '--price', '50'])
        self.assertIn('Room added with id 4', output)
        with open(db.DB_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.assertEqual(len(data['rooms']), 4)

    def test_cli_reserve(self):
        self.run_cli(['init-db'])
        self.run_cli(['add-client', '--name', 'Bob', '--email', 'b@example.com', '--phone', '555'])
        output = self.run_cli([
            'reserve', '--client', '1', '--room', '1',
            '--check-in', '2025-01-01', '--nights', '2', '--total', '200'
        ])
        self.assertIn('Reservation created with id 1', output)
        with open(db.DB_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.assertEqual(len(data['reservations']), 1)

    def test_cli_list_rooms(self):
        self.run_cli(['init-db'])
        output = self.run_cli(['list-rooms'])
        self.assertIn('1: standard', output)
