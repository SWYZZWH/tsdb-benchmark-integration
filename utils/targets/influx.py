from utils.targets.target import TargetInterface


class Influx(TargetInterface):
    def __init__(self):
        self.target = "influx"

    def query_total_metrics(self, start_time, end_time):
        pass
