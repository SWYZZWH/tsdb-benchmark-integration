import os
INFLUX = "influx"
TIMESCALEDB = "timescaledb"
VICTORIA_METRICS = "victoriametrics"
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(ROOT_DIR, "configs")
USE_CASE = ["devops", "cpu-only", "iot"]