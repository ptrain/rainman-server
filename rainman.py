import os
import json

import forecastio
from flask import Flask 

API_KEY = os.environ.get('DARKSKY_API_KEY')
if not API_KEY:
    raise ApiKeyNotFoundError('Please ensure the DARKSKY_API_KEY environment variable is set.')
RAINMAIN_API_KEY = os.environ.get('RAINMAN_API_KEY')
if not RAINMAIN_API_KEY:
    raise ApiKeyNotFoundError('No RAINMAN_API_KEY was configured')

# TODO: In future, we will of course have these as route parameters
BROOKLYN_LAT = 40.69
BROOKLYN_LNG = -73.93

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_rain_data():
    forecast = forecastio.load_forecast(API_KEY, BROOKLYN_LAT, BROOKLYN_LNG)
    byHour = forecast.hourly()
    data = [{'cloudCover': hourData.cloudCover, 'precipProbability': hourData.precipProbability} for hourData in byHour.data[0:24]]
    return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))

if __name__ == '__main__':
    app.run(debug=True)


class ApiKeyNotFoundError(Exception):
    pass
