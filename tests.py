import unittest
import requests
import json
import subprocess
import time


class TestApi(unittest.TestCase):
    def setUp(cls) -> None:
        requests.post('http://127.0.0.1:5000/reset', json={})

    def test_read_all(self):
        r = requests.get('http://127.0.0.1:5000/read', json={})
        response = json.loads(r.text)

        rows = len(response['id'].values())

        self.assertEqual(200, r.status_code)
        self.assertEqual(3000, rows)

    def test_sorted_read(self):
        query = {"sort_column": "id"}

        r = requests.get('http://127.0.0.1:5000/read', json=query)
        response = json.loads(r.text)

        rows = len(response['id'].values())

        self.assertEqual(200, r.status_code)
        self.assertEqual(3000, rows)

    def test_filtering_read(self):
        query = {"sort_column": "id",
                 "filtering": {"column": "id",
                               "operator": "==",
                               "value": 20}
                 }

        r = requests.get('http://127.0.0.1:5000/read', json=query)
        response = json.loads(r.text)

        rows = len(response['id'].values())

        self.assertEqual(200, r.status_code)
        self.assertEqual(1, rows)

    def test_pagination_read(self):
        query = {"sort_column": "id",
                 "pagination": {"offset": 0,
                                "limit": 20}
                 }

        r = requests.get('http://127.0.0.1:5000/read', json=query)
        response = json.loads(r.text)

        rows = list(response['id'].values())

        self.assertEqual(200, r.status_code)
        self.assertEqual(20, len(rows))
        for i in range(20):
            self.assertEqual(i+1, rows[i])

    def test_delete_record(self):
        query = {"id": 1}

        r = requests.post('http://127.0.0.1:5000/delete', json=query)

        status_code = r.status_code

        self.assertEqual(200, status_code)

    def test_update_record(self):
        query = {"id": 1,
                 "first_name": "Ann"}

        r = requests.post('http://127.0.0.1:5000/update', json=query)

        status_code = r.status_code
        record = json.loads(r.text)

        self.assertEqual(200, status_code)
        self.assertEqual("Ann", record['first_name']['0'])
