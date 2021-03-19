from utils.workflow import *


def query_gateway(start, end) -> int:
    return 0


class TestAgent:

    def test_missing_points(self, missing_points_configs):
        print(missing_points_configs)
        assert workflow_standard(missing_points_configs)

    def test_max_qps(self):
        pass
