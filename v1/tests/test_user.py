import json
from .base import BaseTest


class UserTest(BaseTest):
    """
    Runs tests on the user api routes
    """

    def test_new_user_registration(self):
        response = self.client.post(
            self.API_URL + "/user",
            data=self.sample_user_1,
            content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertIn("user registered successfully", str(data))

    def test_get_all_users(self):
        response = self.client.get(self.API_URL + "/user")
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Users", str(data))

    def test_invalid_user_registration(self):
        response = self.client.post(
            self.API_URL + "/user",
            data=self.invalid_user,
            content_type='application/json')
        self.assertEqual(response.status_code, 400)
