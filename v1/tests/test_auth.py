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
            self.API_URL + "/auth/signup",
            data=self.user_with_invalid_data,
            content_type='application/json')

        data=json.loads(response.data)

        self.assertEqual(response.status_code, 400)

    def test_registered_user_login(self):
         self.client.post(
            self.API_URL + "/auth/signup",
            data=self.valid_user,
            content_type='application/json')

         login_response = self.client.post(
            self.API_URL + "/auth/login",
            data=self.registered_user_credencials,
            content_type='application/json')

         data = json.loads(login_response.data)
         self.assertEqual(login_response.status_code,200)
         self.assertIn("access-token",str(data))

    def test_non_registered_user_login(self):
        login_response = self.client.post(
            self.API_URL + "/auth/login",
            data=self.registered_user_credencials,
            content_type='application/json')

        data=json.loads(login_response.data)
        self.assertEqual(login_response.status_code,401)




