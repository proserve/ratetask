import unittest

from app import app

HOST = 'http://localhost:5000'
BASE_API = '{}/api'.format(HOST)

STATUS_API = '{}/status'.format(BASE_API)
RATES_API = '{}/rates'.format(BASE_API)


class TestRoutes(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_hello(self):
        rv = self.app.get(STATUS_API)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.json, {'status': 'ok'})

    def test_empty_location(self):
        rv = self.app.get(RATES_API, query_string={})
        self.assertEqual(rv.status_code, 422)
        message = rv.json["message"]
        self.assertEqual(str(message).lower(), "origin is Required".lower())

    def test_invalid_date(self):
        query_string = {'origin': "ORIGI", 'destination': "DESTI", 'date_from': "2019-12-31", 'date_to': "2019-31-12"}
        rv = self.app.get(RATES_API, query_string=query_string)
        self.assertEqual(rv.status_code, 422)
        message = rv.json["message"]
        self.assertEqual(str(message).lower(), '2019-31-12 should formatted in YYYY-MM-DD'.lower())

    def test_valid_param(self):
        query_string = {"origin": "ORIGI", "destination": "DESTI", "date_from": "2016-01-01", "date_to": "2016-01-10"}
        rv = self.app.get(RATES_API, query_string=query_string)
        self.assertEqual(rv.status_code, 200)
