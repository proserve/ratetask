import unittest
import requests
import json
import sys

HOST = 'http://localhost:5000'
BASE_API = '{}/api'.format(HOST)

STATUS_API = '{}/status'.format(BASE_API)
RATES_API = '{}/rates'.format(BASE_API)


def load_resp(response):
    return json.loads(response.content.decode())


class TestStatusAPI(unittest.TestCase):

    def test_hello(self):
        response = requests.get(STATUS_API)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(load_resp(response), {'status': 'ok'})


class TestRatePI(unittest.TestCase):

    def test_empty_location(self):
        response = requests.get(RATES_API, params={})
        self.assertEqual(response.status_code, 422)
        message = load_resp(response)["message"]
        self.assertEqual(str(message).lower(), "origin is Required".lower())

    def test_invalid_date(self):
        params = {"origin": "ORIGI", "destination": "DESTI", "date_from": "2019-12-31", "date_to": "2019-31-12"}
        response = requests.get(RATES_API, params=params)
        self.assertEqual(response.status_code, 422)
        message = load_resp(response)["message"]
        self.assertEqual(str(message).lower(), '2019-31-12 should formatted in YYYY-MM-DD'.lower())

    def test_valid_param(self):
        params = {"origin": "ORIGI", "destination": "DESTI", "date_from": "2016-01-01", "date_to": "2016-01-10"}
        response = requests.get(RATES_API, params=params)
        self.assertEqual(response.status_code, 200)

