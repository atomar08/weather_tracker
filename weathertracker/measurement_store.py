from .measurement import Measurement
from werkzeug.exceptions import abort

complete_measurement_data = {}
timestamp_list = []

def add_measurement(measurement):
    print("complete_measurement_data: {}".format(complete_measurement_data))
    timestamp = measurement.get_timestamp()

    if timestamp in complete_measurement_data:
        print("found previous measurement")
        prev_measurement = complete_measurement_data[timestamp]
        prev_metrics = prev_measurement.get_metrics()
        prev_metrics.update(measurement.get_metrics())
        complete_measurement_data[timestamp] = prev_measurement
    else:
        print("new measurements")
        complete_measurement_data[timestamp] = measurement
        timestamp_list.append(timestamp)

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
    start_index = end_index = -1
    selected_measurement_lis = []

    if start_date >= end_date or len(timestamp_list) < 2:
        return selected_measurement_lis

    if start_date in timestamp_list:
        start_index = timestamp_list.index(start_date)

    if end_date in timestamp_list:
        end_index = timestamp_list.index(end_date)
    else:
        # Assumption: if end_date not present in 'timestamp_list' then consider last date in list as end date
        end_index = len(timestamp_list) - 1

    if start_index == -1 or end_index == -1:
        return []

    index = start_index
    while index < end_index:
        timestamp = timestamp_list[index]
        selected_measurement_lis.append(complete_measurement_data.get(timestamp))
        index += 1

    print("selected list in query_measurements {}".format(selected_measurement_lis))
    return selected_measurement_lis
