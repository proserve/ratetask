import json
import os
from datetime import datetime

import psycopg2
import requests
from flask.globals import request
from werkzeug.exceptions import UnprocessableEntity

from helpers.helpers import get_rows, compare_date, timeit, exec_query
from helpers.queries import code_query, code_query_new, insert_prices


def get_rates(is_null=False):
    origin, destination, date_from, date_to = check_rate_request()
    return fetch_rates(date_from, date_to, destination, origin, is_null)


def get_rates_new(is_null=False):
    origin, destination, date_from, date_to = check_rate_request()
    return fetch_rates_new(date_from, date_to, destination, origin, is_null)


@timeit
def fetch_rates(date_from, date_to, destination, origin, is_null):
    average_price = 'CASE WHEN count(*) < 3 THEN null ELSE ROUND(AVG(prices.price)) END as average_price' if is_null \
        else 'ROUND(AVG(prices.price), 2) as average_price'
    query = '''
                select to_json(data)
                from (select d.date as day, result.average_price
                    from generate_series('{0}'::timestamp
                     , '{1}'::timestamp
                     , '1 day'::interval) d
                     left outer join (SELECT day, {6} from prices
                        WHERE '[{0}, {1}]'::daterange @> day
                        and (dest_code = '{3}'  or dest_code in ({4}))
                        and (orig_code = '{2}' or orig_code in ({5}))
                      GROUP BY day ORDER BY day ASC) result on d.date = result.day) data;
         '''.format(date_from, date_to, origin, destination, code_query(destination), code_query(origin), average_price)
    items = get_rows(query)
    return [item[0] for item in items]


@timeit
def fetch_rates_new(date_from, date_to, destination, origin, is_null):
    average_price = 'CASE WHEN count(*) < 3 THEN null ELSE ROUND(AVG(prices.price)) END as average_price' if is_null \
        else 'ROUND(AVG(prices.price), 2) as average_price'
    query = '''
                select to_json(data)
                from (select d.date as day, result.average_price
                    from generate_series('{0}'::timestamp
                     , '{1}'::timestamp
                     , '1 day'::interval) d
                     left outer join (SELECT day, {6} from prices
                        WHERE dest_code in {4} and orig_code in {5}
                        GROUP BY day ORDER BY day ASC) result on d.date = result.day) data;
         '''.format(date_from, date_to, origin, destination, code_query_new(destination), code_query_new(origin),
                    average_price)
    items = get_rows(query, True)
    return [item[0] for item in items]


@timeit
def create_rate():
    origin, destination, date_from, date_to, price = check_rate_request(True)
    currency = request.json.get("currency")
    if currency:
        currency = currency.upper()
        try:
            response = requests.get(os.getenv("EXCHANGE_RATES_URL"))
            rates = response.json().get('rates')
            if currency in rates:
                price = int(rates.get(currency) * price)
            else:
                raise UnprocessableEntity(
                    "Invalid currency, here are all the valid currencies {}".format(rates.keys()))
            pass
        except Exception as e:
            raise UnprocessableEntity(str(e))

    try:
        query = insert_prices(destination, origin, date_from, date_to, price)
        exec_query(query)
    except psycopg2.DatabaseError as e:
        raise UnprocessableEntity(str(e))


def check_rate_request(is_post=False):
    def check_date_format(date):
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except:
            raise UnprocessableEntity("{} should formatted in YYYY-MM-DD".format(date))

    def get_not_empty(key):
        value = (request.args and request.args.get(key)) or (request.json and request.json.get(key))
        if value:
            return value
        raise UnprocessableEntity("{} is required".format(key))

    origin = get_not_empty('origin_code' if is_post else 'origin')
    destination = get_not_empty('destination_code' if is_post else 'destination')
    date_from = get_not_empty('date_from')
    date_to = get_not_empty('date_to')

    check_date_format(date_from)
    check_date_format(date_to)
    if compare_date(date_from, date_to) == -1:
        raise UnprocessableEntity("to_date should be higher than from")
    resp = origin, destination, date_from, date_to

    if is_post:
        price = get_not_empty('price' if is_post else 'origin')
        try:
            price = int(price)
        except ValueError as e:
            raise UnprocessableEntity("price should be integer")
        resp = resp + (price,)
    return resp
