from flask import Flask
from flask import request, jsonify
from flask.views import MethodView
from werkzeug.exceptions import abort

from weathertracker.utils.conversion import (
    convert_to_datetime,
    DatetimeConversionException,
)

app = Flask(__name__)
from .measurement import Measurement
from .measurement_store import add_measurement


class MeasurementsAPI(MethodView):
    # features/01-measurements/01-add-measurement.feature
    def post(self):
        if not request.is_json:
            abort(400, "please send request in json format")
        request_data_dic = request.json

        if 'timestamp' not in request_data_dic:
            abort(400, "timestamp field can be empty")

        try:
            timestamp_str = request_data_dic.pop('timestamp')
            timestamp = convert_to_datetime(timestamp_str)
        except DatetimeConversionException as dce:
            print("Error: {}".format(dce))
            abort(400, "improper timestamp format")
        except Exception as e:
            print("improper timestamp {}".format(e))
            abort(400, "invalid timestamp")

        metrics = {}
        for metric, value in request_data_dic.items():
            try:
                print("adding {} and {}".format(metric, value))
                metrics[metric] = float(value)
            except ValueError as e:
                print("value error parsing metric value {}".format(e))
                abort(400, "illegal metric value")
            except Exception as e:
                print("error parsing metric value {}".format(e))
                abort(400, "illegal request")
        add_measurement(Measurement(timestamp, metrics))

        response = jsonify()
        response.status_code = 201
        response.headers['location'] = '/measurements/{}'.format(timestamp_str)
        response.autocorrect_location_header = False
        return response

    # features/01-measurements/02-get-measurement.feature
    def get(self, timestamp):
        try:
            timestamp = convert_to_datetime(timestamp)
        except DatetimeConversionException:
            return abort(400)

        # TODO:
        abort(501)
