import unittest
import json
from ..api import create_app, API_URL


class BaseTest(unittest.TestCase):
    def setUp(self):
        app = create_app()
        self.client = app.test_client()
        self.API_URL = API_URL

        self.sample_entry_1 = json.dumps({
            "title": "this is my first title",
            "content": "as i was writing api tests,..."
        })

        self.sample_entry_2 = json.dumps({
            "title": "title2",
            "content": "this is my story"
        })

        self.modified_sample_entry_1 = json.dumps({
            "title": "this is the new title",
            "content": "and the content is different"
        })

        self.invalid_entry_1 = json.dumps({"title": 1, "content": []})

        self.missing_fields_entry = json.dumps({"content": "abc efg hijk"})

        self.excess_fields_entry = json.dumps({
            "name": "kato jamuel",
            "username": "sandystorm",
            "title": "this is an api",
            "content": "No, this is json."
        })

        self.sample_user_1 = json.dumps({
            "firstname": "raphael",
            "lastname": "kato",
            "username": "rkat",
            "email": "raphkat@gmail.com",
            "password": "raphpass"
        })

        self.invalid_user = json.dumps({
            "firstname": 1,
            "lastname": "peter",
            "username": "1peter",
            "email": "petermail",
            "password": "pass"
        })
