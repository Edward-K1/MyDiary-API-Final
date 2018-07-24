import json
from .base import BaseTest


class DiaryTest(BaseTest):
    """
    Runs tests on the diary api routes
    """

    def test_register_new_diary_entry(self):
        response = self.client.post(
            self.API_URL + "/entry",
            data=self.sample_entry_1,
            content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertIn("new diary entry added", data['message'])

    def test_valid_diary_entry_is_registered_but_excess_fields_are_ignored(self):
        response = self.client.post(
            self.API_URL + "/entry",
            data=self.excess_fields_entry,
            content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertIn("excess fields were ignored", str(data))

    def test_entry_with_missing_fields_returns_bad_request(self):
        response = self.client.post(
            self.API_URL + "/entry",
            data=self.missing_fields_entry,
            content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("The following fields were missing", data['message'])

    def test_get_all_diary_entries(self):
        self.client.post(
            self.API_URL + "/entry",
            data=self.sample_entry_1,
            content_type='application/json')
        self.client.post(
            self.API_URL + "/entry",
            data=self.sample_entry_2,
            content_type='application/json')

        get_response = self.client.get(self.API_URL + "/entry")

        data = json.loads(get_response.data)
        self.assertEqual(get_response.status_code, 200)
        self.assertIn("Diary Entries", data)
        self.assertIn('this is my first title', str(data))

    def test_get_single_diary_entry(self):
        get_response = self.client.get(self.API_URL + "/entry/1")
        self.assertEqual(get_response.status_code, 200)

    def test_get_single_entry_with_invalid_id_returns_not_found(self):
        get_response = self.client.get(self.API_URL + "/entry/1678")
        self.assertEqual(get_response.status_code, 404)

    def test_invalid_data_entry(self):
        response = self.client.post(
            self.API_URL + "/entry",
            data=self.invalid_entry_1,
            content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_user_can_modify_entries(self):

        response = self.client.put(
            self.API_URL + "/entry/1",
            data=self.modified_sample_entry_1,
            content_type='application/json')
        get_response = self.client.get(self.API_URL + "/entry")

        data = json.loads(get_response.data)
        self.assertEqual(response.status_code, 201)
        self.assertIn("this is the new title", str(data))
        self.assertIn("and the content is different", str(data))

    def test_diary_entry_modification_with_invalid_data_returns_bad_request(self):
        response = self.client.put(
            self.API_URL + "/entry/1",
            data=self.invalid_entry_1,
            content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_diary_entry_modification_with_invalid_id_returns_not_found(self):
        response = self.client.put(
            self.API_URL + "/entry/1986",
            data=self.modified_sample_entry_1,
            content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_user_can_delete_entry(self):
        self.client.post(
            self.API_URL + "/entry",
            data=self.sample_entry_1,
            content_type='application/json')

        response = self.client.delete(self.API_URL + "/entry/2")
        self.assertEqual(response.status_code, 200)

    def test_entry_deletion_with_non_existent_id_returns_not_found(self):
        response = self.client.delete(self.API_URL + "/entry/2550")
        self.assertEqual(response.status_code, 404)

