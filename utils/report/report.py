import matplotlib.pyplot as plt
import numpy as np
from functools import reduce
import logging
import os

from definitions import SUPPORTED_TARGETS, SUPPORTED_METRICS


class Result:
    def __init__(self, target, variant_value, test_statistics: dict):
        assert target in SUPPORTED_TARGETS
        for k in test_statistics.keys():
            assert k in SUPPORTED_METRICS

        self.target = target
        self.variant_value = variant_value
        self.test_statistics = test_statistics

    def get_target(self):
        return self.target

    def get_variant_value(self):
        return self.variant_value

    def get_test_statistics(self):
        return self.test_statistics


class Report:

    def __init__(self, title, variant):
        self.title = title
        self.variant_name = variant
        self.results = []

    def add_result(self, result: Result) -> bool:
        assert result.target in SUPPORTED_TARGETS
        for k in result.test_statistics.keys():
            assert k in SUPPORTED_METRICS
        # e.g.
        # self.results = [
        #    (1, {"influx":{"cpu":30, "memory": 50}, "timescaledb":{"cpu":30, "memory": 50}} ),
        #    (10, {"influx":{"cpu":30, "memory": 50}, "timescaledb":{"cpu":30, "memory": 50}} ),
        # ]
        for r in self.results:
            if r[0] == result.variant_value:
                r[1][result.target] = result.test_statistics
                return True

        self.results.append((result.variant_value, {result.target: result.test_statistics}))
        sorted(self.results, key=lambda x: x[0])

    def _get_common_targets(self) -> set:
        # e.g.
        # self.results = [
        #    (1, {"influx":{"cpu":30, "memory": 50}, "timescaledb":{"cpu":30, "memory": 50}} ),
        #    (10, {"timescaledb":{"cpu":30, "memory": 50}}),
        # ]
        # in this situation, _get_targets will return ("timescaledb")
        return reduce(lambda s1, s2: set(s1) & set(s2),
                      [result[1].keys() for result in self.results])

    def _get_common_metrics(self) -> set:
        # e.g.
        # self.results = [
        #    (1, {"influx":{"cpu":30}, "timescaledb":{"cpu":30, "memory": 50}} ),
        #    (10, {"influx":{"cpu":30, "memory": 50}, "timescaledb":{"cpu":30, "memory": 50}} ),
        # ]
        # in this situation, _get_targets will return ("cpu")
        return reduce(lambda s1, s2: set(s1) & set(s2),
                      [statistics.keys() for result in self.results for statistics in result[1].values()])

    def _print_pic(self, save_name, metric, targets):
        with plt.style.context(["science"]):
            fig, ax = plt.subplots()
            # plt.style.use(["science"])

            bar_count = len(targets)
            x = np.arange(len(self.results))
            width = 0.5 * 1 / bar_count

            # ax.set_title(self.title)
            ax.set_xlabel(self.variant_name)
            ax.set_ylabel(metric.replace("_", "-"))
            ax.set_xticks(x)
            ax.set_xticklabels([result[0] for result in self.results])

            for i, target in enumerate(targets):
                ax.bar(x - ((bar_count - 1) / 2 - i) * width, height=[result[1][target][metric] for result in self.results],
                       width=width, label=target)

            ax.legend()
            plt.savefig(save_name)
            plt.show()

            logging.info("pic has been stored in {}".format(save_name))

    def print_pics(self, save_dir):
        save_dir = os.join(save_dir, "results")
        if not os.path.isdir(save_dir):
            os.mkdir(save_dir)

        common_targets = self._get_common_targets()
        common_metrics = self._get_common_metrics()
        if len(common_targets) == 0 or len(common_metrics) == 0:
            logging.info("no pic to draw!!")
            return

        # x_pos = np.arange(len(targets))
        # width = 1 / (len(targets) + 1)

        for metric in common_metrics:
            self._print_pic(os.path.join(save_dir, "_".join([self.title, metric]) + ".png"), metric, common_targets)


if __name__ == "__main__":
    r = Report("empty", "scale")
    r.results = [
        (1, {"influx": {"cpu": 30}, "timescaledb": {"cpu": 30, "memory": 50}}),
        (10, {"influx": {"cpu": 30, "memory": 50}, "timescaledb": {"cpu": 30, "memory": 50}}),
    ]
    assert "cpu" in r._get_common_metrics() and "memory" not in r._get_common_metrics()

    r = Report("empty", "scale")
    r.results = [
        (1, {"influx": {"cpu": 30, "memory": 50}, "timescaledb": {"cpu": 30, "memory": 50}}),
        (10, {"timescaledb": {"cpu": 30, "memory": 50}}),
    ]
    assert "timescaledb" in r._get_common_targets() and "influx" not in r._get_common_targets()

    r = Report("empty", "scale")
    r1 = Result("influx", 1, {"cpu_usage": 30, "memory_usage": 50})
    r2 = Result("influx", 4, {"cpu_usage": 60, "memory_usage": 100})
    r7 = Result("influx", 10, {"cpu_usage": 70, "memory_usage": 120})
    r3 = Result("timescaledb", 1, {"cpu_usage": 10, "memory_usage": 20})
    r4 = Result("timescaledb", 4, {"cpu_usage": 20, "memory_usage": 40})
    r8 = Result("timescaledb", 10, {"cpu_usage": 40, "memory_usage": 70})
    r5 = Result("victoriametrics", 1, {"cpu_usage": 10, "memory_usage": 20})
    r6 = Result("victoriametrics", 4, {"cpu_usage": 20, "memory_usage": 40})
    r9 = Result("victoriametrics", 10, {"cpu_usage": 30, "memory_usage": 100})
    r.add_result(r1)
    r.add_result(r2)
    r.add_result(r3)
    r.add_result(r4)
    r.add_result(r5)
    r.add_result(r6)
    r.print_pics(os.path.join(os.path.abspath(os.path.dirname(__file__))))
