import abc


class TargetInterface:
    @abc.abstractmethod
    def query_total_metrics(self, start_time, end_time):
        pass
