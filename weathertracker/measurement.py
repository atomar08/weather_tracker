class Measurement:
    def __init__(self, timestamp, metrics=None):
        if metrics is None:
            metrics = {}
        self.timestamp = timestamp
        self.metrics = metrics

    def set_metric(self, metric, value):
        self.metrics[metric] = value

    def get_metric(self, metric):
        return self.metrics[metric]

    def get_timestamp(self):
        return self.timestamp

    def get_metrics(self):
        return self.metrics
