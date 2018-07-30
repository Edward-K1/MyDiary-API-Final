import json
from .base import BaseTest


class AuthTest(BaseTest):
    """
    Tests the user authentication routes /auth/*
    """

    def test_valid_user_signup(self):
        response = self.client.post(
            self.API_URL + "/auth/signup",
            data=self.valid_user,
            content_type='application/json')

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertIn("user registered successfully", str(data))

    def test_user_signup_with_missing_fields_returns_bad_request(self):
        response = self.client.post(
            self.API_URL + "/auth/signup",
            data=self.user_with_missing_fields,
            content_type='application/json')

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("The following fields were missing", str(data))

    def test_user_signup_with_invalid_data_returns_bad_request(self):
        response = self.client.post(
            self.API_URL + "/user",
            data=self.user_with_invalid_data,
            content_type='application/json')

        self.assertEqual(response.status_code, 400)
