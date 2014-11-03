import os
import json

import forecastio
from flask import Flask, abort

API_KEY = os.environ.get('DARKSKY_API_KEY')
if not API_KEY:
    raise ApiKeyNotFoundError('Please ensure the DARKSKY_API_KEY environment variable is set.')
RAINMAN_API_KEY = os.environ.get('RAINMAN_API_KEY')
if not RAINMAN_API_KEY:
    raise ApiKeyNotFoundError('No RAINMAN_API_KEY was configured')

# TODO: In future, we will of course have these as route parameters
BROOKLYN_LAT = 40.69
BROOKLYN_LNG = -73.93

app = Flask(__name__)

@app.route('/<api_key>', methods=['GET'])
def get_rain_data(api_key):
    if api_key != RAINMAN_API_KEY:
        abort(401)
    forecast = forecastio.load_forecast(API_KEY, BROOKLYN_LAT, BROOKLYN_LNG)
    byHour = forecast.hourly()
    data = [{'cloudCover': hourData.cloudCover, 'precipProbability': hourData.precipProbability} for hourData in byHour.data[0:24]]
    return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))

if __name__ == '__main__':
    rainman_debug = os.environ.get('RAINMAN_DEBUG', False)
    app.run(debug=rainman_debug)


class ApiKeyNotFoundError(Exception):
    pass
