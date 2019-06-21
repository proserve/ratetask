from flask import Flask, jsonify

from controllers.rate_controller import get_rates, get_rates_new, create_rate


def init(app):
    @app.route('/api/status')
    def status():
        return jsonify({'status': 'ok'})

    @app.route('/api/rates')
    def rates():
        return jsonify(get_rates(False))

    @app.route('/api/rates_new')
    def rates_new():
        return jsonify(get_rates_new(False))

    @app.route('/api/rates_null')
    def rates_null():
        return jsonify(get_rates(True))

    @app.route('/api/rates_null_new')
    def rates_null_new():
        return jsonify(get_rates_new(True))

    # POST
    @app.route('/api/rates', methods=['POST'])
    def create_rates():
        create_rate()
        return "", 201
