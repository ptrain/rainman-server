import os

import forecastio
from flask import Flask 

API_KEY = os.environ.get('DARKSKY_API_KEY')
if not API_KEY:
    raise ApiKeyNotFoundError('Please ensure the DARKSKY_API_KEY environment variable is set.')

app = Flask(__name__)

@app.route('/')
def get_rain_data():
    return "It's GONE RAIN"

if __name__ == '__main__':
    app.run(debug=True)


class ApiKeyNotFoundError(Exception):
    pass