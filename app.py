from flask import Flask, request
from flask.json import jsonify

from exceptions import JSONExceptionHandler
from helpers import check_rate_request, get_rows
from queries import code_query

app = Flask(__name__)
handler = JSONExceptionHandler(app)


@app.route('/api/status')
def hello_world():
    return jsonify({'status': 'ok'})


@app.route('/api/rates')
def rates():
    origin, destination, date_from, date_to = check_rate_request()
    # TODO: should use params binding instead of string formatting to avoid SQL injections
    query = '''
            select to_json(row)
            from (SELECT day, ROUND(AVG(prices.price), 2) as average_price from prices
                  WHERE '[{0}, {1}]'::daterange @> day
                    and (dest_code = '{3}'  or dest_code in ({4}))
                    and (orig_code = '{2}' or orig_code in ({5}))
                  GROUP BY day ORDER BY day DESC) row;
     '''.format(date_from, date_to, origin, destination, code_query(destination), code_query(origin))

    items = get_rows(query)
    return jsonify([item[0] for item in items])


@app.route('/api/rates_null')
def rates_null():
    origin, destination, date_from, date_to = check_rate_request()
    # TODO: should use params binding instead of string formatting to avoid SQL injections
    query = '''
            select to_json(row)
            from (SELECT day, CASE WHEN count(*) < 3 THEN null ELSE ROUND(AVG(prices.price)) END as average_price
                  from prices WHERE '[{0}, {1}]'::daterange @> day
                    and (dest_code = '{3}' or dest_code in ({4}))
                    and (orig_code = '{2}' or orig_code in ({5}))
                  GROUP BY day ORDER BY day DESC) row;
     '''.format(date_from, date_to, origin, destination, code_query(destination), code_query(origin))

    items = get_rows(query)
    return jsonify([item[0] for item in items])


if __name__ == '__main__':
    app.run()
