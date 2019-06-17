import os
from datetime import datetime

import psycopg2
from dotenv.main import load_dotenv
from werkzeug.exceptions import UnprocessableEntity

from flask import request
from werkzeug.exceptions import BadRequest


def parse_date_in_request(key):
    try:
        date = request.args.get(key)
        return datetime.strptime(date, '%Y-%m-%d')
    except:
        raise BadRequest("{} should formatted in YYYY-MM-DD")


def check_rate_request():
    def check_date_format(date):
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except:
            raise UnprocessableEntity("{} should formatted in YYYY-MM-DD".format(date))

    def get_not_empty(key):
        value = request.args.get(key)
        if value:
            return value
        raise UnprocessableEntity("{} is required".format(key))

    origin = get_not_empty('origin')
    destination = get_not_empty("destination")
    date_from = get_not_empty('date_from')
    date_to = get_not_empty('date_to')

    check_date_format(date_from)
    check_date_format(date_to)
    return origin, destination, date_from, date_to


def get_db_connection():
    load_dotenv()
    return psycopg2.connect(user=os.getenv("DB_USERNAME"),
                            host=os.getenv("DB_HOST"),
                            database=os.getenv('DB_NAME'))


def get_rows(query, params=None):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(query, params)
    return cur.fetchall()