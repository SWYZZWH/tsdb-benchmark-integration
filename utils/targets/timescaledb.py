from utils.targets.target import TargetInterface


class Timescaledb(TargetInterface):
    def __init__(self):
        self.target = "timescaledb"

    def query_total_metrics(self, start_time, end_time):
        pass
