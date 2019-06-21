import os
from datetime import datetime
from time import time

import psycopg2
from dotenv.main import load_dotenv


def compare_date(to_date, from_date):
    _from_date = datetime.strptime(to_date, '%Y-%m-%d')
    _to_date = datetime.strptime(from_date, '%Y-%m-%d')

    if (_to_date - _from_date).days == 0:
        return 0

    if (_to_date - _from_date).days < 0:
        return -1

    if (_to_date - _from_date).days > 0:
        return 1


def get_db_connection(is_new):
    load_dotenv()
    db_name = 'rates' if is_new else 'postgres'
    return psycopg2.connect(user=os.getenv("DB_USERNAME"),
                            host=os.getenv("DB_HOST"),
                            database=db_name)


def get_rows(query, is_new=False):
    conn = get_db_connection(is_new)
    cur = conn.cursor()
    cur.execute(query, {})
    return cur.fetchall()


def exec_query(query, is_new=False):
    conn = get_db_connection(is_new)
    cur = conn.cursor()
    cur.execute(query, {})
    conn.commit()


def timeit(method):
    def timed(*args, **kw):
        ts = time()
        result = method(*args, **kw)
        te = time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print('%r  %2.2f ms' % \
                  (method.__name__, (te - ts) * 1000))
        return result

    return timed
