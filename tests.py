import unittest
import requests
import json
import subprocess
import time


class TestApi(unittest.TestCase):
    def setUp(cls) -> None:
        """ Reload the server's data store from it's datafile before each test."""
        requests.post('http://127.0.0.1:5000/reset', json={})

    def test_read_all(self):
        """ Read all requirement"""
        r = requests.get('http://127.0.0.1:5000/read', json={})
        response = json.loads(r.text)

        rows = len(response['id'].values())

        self.assertEqual(200, r.status_code)
        self.assertEqual(3000, rows)

    def test_sorted_read(self):
        """Sorted reading requirement"""
        query = {"sort_column": "id"}

        r = requests.get('http://127.0.0.1:5000/read', json=query)
        response = json.loads(r.text)

        rows = len(response['id'].values())

        self.assertEqual(200, r.status_code)
        self.assertEqual(3000, rows)

    def test_filtering_read(self):
        """Filtering reading requirement.
           Read one record requirement."""
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
        """ Pagination reading requirement."""
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
        """ Delete record requirement."""
        query = {"id": 1}

        r = requests.post('http://127.0.0.1:5000/delete', json=query)

        status_code = r.status_code

        self.assertEqual(200, status_code)

    def test_update_record(self):
        """ Update record requirement."""
        query = {"id": 1,
                 "first_name": "Ann"}

        r = requests.post('http://127.0.0.1:5000/update', json=query)

        status_code = r.status_code
        record = json.loads(r.text)

        self.assertEqual(200, status_code)
        self.assertEqual("Ann", record['first_name']['0'])

    def test_get_average_age_by_industry(self):
        """ Age per industry requirement"""
        query = {"target_column": "age",
                 "category": "industry"}

        r = requests.post('http://127.0.0.1:5000/average_by', json=query)

        status_code = r.status_code
        result = json.loads(r.text)

        self.assertEqual(200, status_code)
        self.assertEqual(75, result['category']['Diversified Financial Services']['mean'])

    def test_get_average_salary_by_industry(self):
        """ Salary per industry requirement"""
        query = {"target_column": "salary",
                 "category": "industry"}

        r = requests.post('http://127.0.0.1:5000/average_by', json=query)

        status_code = r.status_code
        result = json.loads(r.text)

        self.assertEqual(200, status_code)
        self.assertEqual(143500.79, result['category']['Diversified Financial Services']['mean'])

    def test_get_average_salary_by_experience(self):
        """ Salary per years experience requirement"""
        query = {"target_column": "salary",
                 "category": "years_of_experience"}

        r = requests.post('http://127.0.0.1:5000/average_by', json=query)

        status_code = r.status_code
        result = json.loads(r.text)

        print("result", result)
        self.assertEqual(200, status_code)
        self.assertEqual(143401.94456790123, result['category']["6.0"]['mean'])

    def test_get_stats(self):
        """ 'Interesting Stats' requirement."""
        query = {"category": "years_of_experience"}

        r = requests.post('http://127.0.0.1:5000/describe_column', json=query)

        status_code = r.status_code
        result = json.loads(r.text)

        self.assertEqual(200, status_code)
        self.assertEqual(35, result['max'])


if __name__ == "__main__":
    unittest.main()