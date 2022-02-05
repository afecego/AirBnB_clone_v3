#!/usr/bin/python3
"""
Create an api
"""

from os import getenv
from api.v1.views import app_views
from models import storage
from flask import Flask, jsonify, make_response

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """ Close session """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ Handle not found page """
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(host=getenv('HBNB_API_HOST', '0.0.0.0'),
            port=getenv('HBNB_API_PORT', '5000'), threaded=True)
