import os

INFLUX = "influx"
TIMESCALEDB = "timescaledb"
VICTORIA_METRICS = "victoriametrics"
SUPPORTED_TARGETS = {INFLUX, TIMESCALEDB, VICTORIA_METRICS}
SUPPORTED_METRICS = ["cpu_usage", "memory_usage"]
BASE_URL = "http://localhost:2375"
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(ROOT_DIR, "configs")
USE_CASE = ["devops", "cpu-only", "iot"]