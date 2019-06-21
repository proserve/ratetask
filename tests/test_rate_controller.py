import unittest
from datetime import datetime, timedelta

from werkzeug.exceptions import UnprocessableEntity

from app import app
from controllers.rate_controller import check_rate_request, fetch_rates, fetch_rates_new


class TestController(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_check_rate_request_success(self):
        url = '/?origin=CNNBO&destination=NOGJM&date_from=2016-01-01&date_to=2016-01-30'
        with app.test_request_context(url):
            app.preprocess_request()
            origin, destination, date_from, date_to = check_rate_request()
            assert origin == "CNNBO"
            assert destination == "NOGJM"
            assert date_from == "2016-01-01"
            assert date_to == "2016-01-30"

    def test_check_rate_request_is_required(self):
        url = '/?destination=NOGJM&date_from=2016-01-01&date_to=2016-01-30'
        with app.test_request_context(url):
            app.preprocess_request()
            try:
                check_rate_request()
                assert False
            except UnprocessableEntity as e:
                assert e.description.lower() == "origin is required"

    def test_check_rate_request_is_date_formatted(self):
        wrong_date = '2016-31-01'
        url = '/?origin=CNNBO&destination=NOGJM&date_from=%s&date_to=2016-01-30' % wrong_date
        with app.test_request_context(url):
            app.preprocess_request()
            try:
                check_rate_request()
                assert False
            except UnprocessableEntity as e:
                assert e.description.lower() == ('%s should formatted in yyyy-mm-dd' % wrong_date)

    def test_check_rate_request_is_date_range(self):
        url = '/?origin=CNNBO&destination=NOGJM&date_from=2016-01-31&date_to=2016-01-20'
        with app.test_request_context(url):
            app.preprocess_request()
            try:
                check_rate_request()
                assert False
            except UnprocessableEntity as e:
                assert e.description.lower() == 'to_date should be higher than from'

    def test_fetch_rates_empty_dest_china(self):
        date_from = '2016-01-01'
        date_to = '2016-01-30'
        rates = fetch_rates(date_from, date_to, 'china_main', 'northern_europe', False)
        assert len(rates) == 30
        for index, rate in enumerate(rates):
            assert datetime.strptime(rate['day'], '%Y-%m-%d') - datetime.strptime(date_from, '%Y-%m-%d') == timedelta(
                days=index)

            assert rate['average_price'] is None

    def test_fetch_rates_empty_dest_china_new(self):
        date_from = '2016-01-01'
        date_to = '2016-01-30'
        rates = fetch_rates_new(date_from, date_to, 'china_main', 'northern_europe', False)
        assert len(rates) == 30
        for index, rate in enumerate(rates):
            assert datetime.strptime(rate['day'], '%Y-%m-%d') - datetime.strptime(date_from, '%Y-%m-%d') == timedelta(
                days=index)

            assert rate['average_price'] is None

    def test_fetch_rates_less_than_3_new(self):
        date_from = '2016-01-24'
        date_to = '2016-01-26'
        origin = 'CNCWN'
        destination = 'DKFRC'
        rates = fetch_rates_new(date_from, date_to, destination, origin, True)
        assert len(rates) == 3
        assert rates[0]['average_price'] is None
        assert rates[1]['average_price'] == 1039
        assert rates[2]['average_price'] is None


if __name__ == '__main__':
    unittest.main()

