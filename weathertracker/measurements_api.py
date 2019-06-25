from flask import Flask
from flask import request
from flask.views import MethodView
from werkzeug.exceptions import abort

from weathertracker.utils.conversion import (
    convert_to_datetime,
    DatetimeConversionException,
)

app = Flask(__name__)
from .measurement import Measurement
from .measurement_store import add_measurement
from flask import Response


class MeasurementsAPI(MethodView):
    # features/01-measurements/01-add-measurement.feature
    @app.route('/measurements/', methods=['POST'])
    def post(self):
        if not request.is_json:
            abort(400, "please send request in json format")
        request_data_dic = request.json

        if 'timestamp' not in request_data_dic:
            abort(400, "timestamp field can be empty")

        timestamp = request_data_dic.pop('timestamp')
        metrics = {}
        for metric, value in request_data_dic.items():
            try:
                print("adding {} and {}".format(metric, value))
                metrics[metric] = float(value)
            except ValueError as e:
                print("value error parsing metric value {}".format(e))
            except Exception as e:
                print("error parsing metric value {}".format(e))
        add_measurement(Measurement(timestamp, metrics))

        return Response(status=201)
        # return Response("{'a':'b'}", status=201, mimetype='application/json')
        # abort(501)

    # features/01-measurements/02-get-measurement.feature
    def get(self, timestamp):
        try:
            timestamp = convert_to_datetime(timestamp)
        except DatetimeConversionException:
            return abort(400)

        # TODO:
        abort(501)
