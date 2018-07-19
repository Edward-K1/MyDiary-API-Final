import unittest
import json
from ..api import create_app, API_URL


class BaseTest(unittest.TestCase):
    def setUp(self):
        app=create_app()
        self.client= app.test_client()
        self.API_URL = API_URL

        self.sample_entry_1 = json.dumps({
            "title": "this is my first title",
            "content":"as i was writing api tests,..."
        })

        self.sample_entry_2 = json.dumps({
            "title": "title2",
            "content": "this is my story"
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

class DiaryTest(BaseTest):
    """
    Runs Tests on the diary api endpoints
    """

    def test_register_new_diary_entry(self):
        response = self.client.post(self.API_URL+"/entry",data=self.sample_entry_1,content_type='application/json')
        data=json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertIn("new diary entry added",data['message'])

    def test_get_diary_entries(self):
        response1=self.client.post(self.API_URL+"/entry",data=self.sample_entry_1,content_type='application/json')
        response1=self.client.post(self.API_URL+"/entry",data=self.sample_entry_2,content_type='application/json')

        get_response=self.client.get(self.API_URL+"/entry")
        data=json.loads(get_response.data)
        self.assertEqual(get_response.status_code,200)

if __name__ == '__main__':
    unittest.main()
