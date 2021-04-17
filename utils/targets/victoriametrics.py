from utils.targets.target import TargetInterface


class Victoriametrics(TargetInterface):
    def __init__(self):
        self.target = "victoriametrics"

    def query_total_metrics(self, start_time, end_time):
        pass
