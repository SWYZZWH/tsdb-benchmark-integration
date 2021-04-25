import matplotlib.pyplot as plt
import numpy as np
from functools import reduce
import logging
import os
import statistics as stt

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
        self.valid = True

    def add_result(self, result: Result, is_valid) -> bool:
        assert result.target in SUPPORTED_TARGETS

        if not is_valid:
            self.valid = False

        for k in result.test_statistics.keys():
            assert k in SUPPORTED_METRICS

        for r in self.results:
            if r[0] == result.variant_value:
                r[1][result.target] = result.test_statistics
                return True

        self.results.append((result.variant_value, {result.target: result.test_statistics}))
        sorted(self.results, key=lambda x: x[0])

    def _get_common_targets(self) -> set:
        # e.g.
        # self.results = [
        #    (1, {"influx":{"cpu":[30, 40]}, "timescaledb":{"cpu":[30, 40], "memory": [30, 40]}} ),
        #    (10, {"timescaledb":{"cpu":[30, 40], "memory": [30, 40]}} ),
        # ]
        # in this situation, _get_targets will return ("timescaledb")
        return reduce(lambda s1, s2: set(s1) & set(s2),
                      [result[1].keys() for result in self.results])

    def _get_common_metrics(self) -> set:
        # e.g.
        # self.results = [
        #    (1, {"influx":{"cpu":[30, 40]}, "timescaledb":{"cpu":[30, 40], "memory": [30, 40]}} ),
        #    (10, {"influx":{"cpu":[30, 40], "memory": [30, 40]}, "timescaledb":{"cpu":[30, 40], "memory": [30, 40]}} ),
        # ]
        # in this situation, _get_targets will return ("cpu")
        return reduce(lambda s1, s2: set(s1) & set(s2),
                      [statistics.keys() for result in self.results for statistics in result[1].values()])

    def _print_bar_graph(self, save_name, metric, targets):

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
                ax.bar(x - ((bar_count - 1) / 2 - i) * width, height=[stt.mean(result[1][target][metric]) for result in self.results],
                       width=width, label=target)

            ax.legend()
            plt.savefig(save_name)
            plt.show()

            logging.info("pic has been stored in {}".format(save_name))

    def print_pics(self, save_dir):
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
            self._print_bar_graph(os.path.join(save_dir, "_".join([self.title, metric]) + ".png"), metric, common_targets)
            # self._print_line_chart(os.path.join(save_dir, "_".join([self.title, metric]) + ".png"), metric, common_targets)

    def export_results(self, save_dir):
        with open(os.path.join(save_dir, "_".join([self.title]) + ".txt"), "w") as f:
            f.write("this test result is " + ("valid" if self.valid else "invalid") + "\n")
            f.write(self.results.__str__())

    def generate_report(self, save_dir):
        save_dir = os.path.join(save_dir, "results")
        self.print_pics(save_dir)
        self.export_results(save_dir)


if __name__ == "__main__":
    r = Report("empty", "scale")
    r.results = [
        (1, {"influx": {"cpu": [30, 40]}, "timescaledb": {"cpu": [30, 40], "memory": [30, 50]}}),
        (10, {"influx": {"cpu": [30, 20], "memory": [30, 50]}, "timescaledb": {"cpu": [30, 30], "memory": [30, 50]}}),
    ]
    assert "cpu" in r._get_common_metrics() and "memory" not in r._get_common_metrics()

    r = Report("empty", "scale")
    r.results = [
        (1, {"influx": {"cpu": [30, 50], "memory": [30, 50]}, "timescaledb": {"cpu": [30, 20], "memory": [30, 100]}}),
        (10, {"timescaledb": {"cpu": [30, 50], "memory": [30, 450]}}),
    ]
    assert "timescaledb" in r._get_common_targets() and "influx" not in r._get_common_targets()

    r = Report("empty", "scale")
    r1 = Result("influx", 1, {"cpu_usage": [30, 50], "memory_usage": [30, 50]})
    r2 = Result("influx", 4, {"cpu_usage": [30, 50], "memory_usage": [30, 50]})
    r7 = Result("influx", 10, {"cpu_usage": [30, 50], "memory_usage": [30, 50]})
    r3 = Result("timescaledb", 1, {"cpu_usage": [30, 50], "memory_usage": [30, 50]})
    r4 = Result("timescaledb", 4, {"cpu_usage": [30, 50], "memory_usage": [30, 50]})
    r8 = Result("timescaledb", 10, {"cpu_usage": [30, 50], "memory_usage": [30, 50]})
    r5 = Result("victoriametrics", 1, {"cpu_usage": [30, 50], "memory_usage": [30, 50]})
    r6 = Result("victoriametrics", 4, {"cpu_usage": [30, 50], "memory_usage": [30, 50]})
    r9 = Result("victoriametrics", 10, {"cpu_usage": [30, 50], "memory_usage": [30, 50]})
    r.add_result(r1)
    r.add_result(r2)
    r.add_result(r3)
    r.add_result(r4)
    r.add_result(r5)
    r.add_result(r6)
    r.print_pics(os.path.join(os.path.abspath(os.path.dirname(__file__))))
