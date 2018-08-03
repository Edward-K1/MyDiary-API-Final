import unittest
import json
from ..api import create_app, API_URL
from ..api.db import DatabaseManager


class BaseTest(unittest.TestCase):
    def setUp(self):
        DatabaseManager.drop_tables()
        app = create_app()
        self.client = app.test_client()
        self.API_URL = API_URL

        DatabaseManager.create_tables()

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

        self.valid_user = json.dumps({
            "firstname": "raphael",
            "lastname": "kato",
            "username": "rkat",
            "email": "raphkat@gmail.com",
            "password": "raphpass"
        })

        self.user_with_missing_fields = json.dumps({
            "fir": "ronald",
            "la": "kimera",
            "user": "rkat",
            "email": "patopha@gmail.com",
            "password": "letthisbe"
        })


        self.user_with_invalid_data = json.dumps({
            "firstname": "1",
            "lastname": "peter",
            "username": "1peter",
            "email": "petermail",
            "password": "pass"
        })

        self.registered_user_credencials = json.dumps({
            "email": "raphkat@gmail.com",
            "password": "raphpass"
        })

        self.non_registered_user_credencials = json.dumps({
            "email": "logme@wooly.com",
            "password": "mypasswillpass"
        })

    def mock_login(self):
        self.client.post(
            self.API_URL + "/auth/signup",
            data=self.valid_user,
            content_type='application/json')

        login_response = self.client.post(
            self.API_URL + "/auth/login",
            data=self.registered_user_credencials,
            content_type='application/json')

        data = json.loads(login_response.data)

        return data

    def create_headers(self,token):
        return {'Content-Type':'application/json','access-token':token}


    def tearDown(self):
        DatabaseManager.drop_tables()

