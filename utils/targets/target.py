import abc


class TargetInterface:
    @abc.abstractmethod
    def query_total_metrics(self):
        pass
