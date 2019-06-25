from .measurement import Measurement
from werkzeug.exceptions import abort

complete_measurement_data = {}


def add_measurement(measurement):
    print("complete_measurement_data: {}".format(complete_measurement_data))
    timestamp = measurement.get_timestamp()
    print("adding {} metrics, type {}".format(timestamp, type(timestamp)))

    if timestamp in complete_measurement_data:
        print("found previous measurement")
        prev_measurement = complete_measurement_data[timestamp]
        prev_metrics = prev_measurement.get_metrics()
        prev_metrics.update(measurement.get_metrics())
        complete_measurement_data[timestamp] = prev_measurement
    else:
        print("new measurements")
        complete_measurement_data[timestamp] = measurement

    # for debugging purpose:
    print("Current complete_measurement_data")
    for timestamp, measurement in complete_measurement_data.items():
        print("For timestamp: {}".format(timestamp))
        for metric, value in measurement.get_metrics().items():
            print("metric: {}, value: {}".format(metric, value))
    return


def get_measurement(date):
    result = {}
    if date not in complete_measurement_data:
        print("timestamp {} not present, type {}".format(date, type(date)))
        return result
    else:
        measurement = complete_measurement_data[date]
        print("found info, timestamp {}, type {}".format(measurement.get_timestamp(), type(measurement.get_timestamp())))
        result['timestamp'] = measurement.get_timestamp()
        result.update(measurement.get_metrics())
        return result


def query_measurements(start_date, end_date):
    # TODO:
    abort(501)
