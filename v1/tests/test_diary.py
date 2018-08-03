""" This module runs tests on the diary endpoint routes """
import json
from .base import BaseTest


class TestDiary(BaseTest):
    """
    Runs tests on the diary api routes
    """

    def test_creation_of_new_diary_entry(self):
        data = self.mock_login()
        token=data['access-token']

        response = self.client.post(
            self.API_URL + "/entries",
            data=self.sample_entry_1,
            headers=self.create_headers(token))
        data=json.loads(response.data)

        self.assertEqual(response.status_code,201)
        self.assertIn("new diary entry added",str(data))

    def test_creation_of_new_entry_with_missing_fields_returns_400(self):
        data = self.mock_login()
        token=data['access-token']

        response = self.client.post(
            self.API_URL + "/entries",
            data=self.missing_fields_entry,
            headers=self.create_headers(token))
        data=json.loads(response.data)
        self.assertEqual(response.status_code,400)

    def test_get_all_diary_entries(self):
        data = self.mock_login()
        token=data['access-token']

        self.client.post(
            self.API_URL + "/entries",
            data=self.sample_entry_1,
            headers=self.create_headers(token))

        response=self.client.get(
            self.API_URL + "/entries",
            headers=self.create_headers(token))

        data=json.loads(response.data)
        self.assertEqual(response.status_code,200)

    def test_get_single_entry(self):
        data = self.mock_login()
        token=data['access-token']

        self.client.post(
            self.API_URL + "/entries",
            data=self.sample_entry_1,
            headers=self.create_headers(token))

        response=self.client.get(
            self.API_URL + "/entries/1",
            headers=self.create_headers(token))

        data=json.loads(response.data)
        self.assertEqual(response.status_code,200)

    def test_update_diary_entry(self):
        data = self.mock_login()
        token=data['access-token']

        self.client.post(
            self.API_URL + "/entries",
            data=self.sample_entry_1,
            headers=self.create_headers(token))

        response=self.client.put(
            self.API_URL + "/entries/1", data=self.modified_sample_entry_1,
            headers=self.create_headers(token))

        data=json.loads(response.data)
        self.assertEqual(response.status_code,202)

    def test_delete_diary_entry(self):
        data = self.mock_login()
        token=data['access-token']

        self.client.post(
            self.API_URL + "/entries",
            data=self.sample_entry_1,
            headers=self.create_headers(token))

        response=self.client.delete(
            self.API_URL + "/entries/1",
            headers=self.create_headers(token))

        data=json.loads(response.data)
        self.assertEqual(response.status_code,200)



