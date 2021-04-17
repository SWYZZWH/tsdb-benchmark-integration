from datetime import datetime, timedelta

from pyrfc3339 import generate, parse
import logging

# how many rows are reported by single host every reporting period in specific use-case
use_case_rows_count = {"devops": 9, "cpu-only": 1, "iot": 1.8}

# how many metrics are reported by single host every reporting period in specific use-case
use_case_metrics_count = {"devops": 100, "cpu-only": 10, "iot": 14}

# how many metrics can be handled by each tsdb approximately
processing_capacity_in_metrics = {"influx": 300 * 1000, "timescaledb": 300 * 1000, "victoriametrics": 300 * 1000}


def autoset_timestamp_end(params: dict):
    scale = params.get("scale")
    if scale is None:
        logging.error("scale is not set!!")
        return

    expected_test_duration = params.get("expected-test-duration")
    if expected_test_duration is None:
        logging.info("auto set timestamp_end is disabled")
        return

    qps = 300 * 1000
    if params.get("limiter-max-qps") is not None and params.get("use-qps-limiter") is not None and params.get("use-qps-limiter") is True:
        qps = params.get("limiter-max-qps")
    usecase = params.get("use-case") if params.get("use-case") in use_case_metrics_count.keys() else "devops"
    log_interval = params.get("log_interval") if params.get("log_interval") is not None else 10
    timestamp_start = params.get("timestamp-start") if params.get(
        "timestamp-start") is not None else "2020-01-01T00:00:00Z"

    timestamp_start = parse(timestamp_start)
    delta_time = log_interval * expected_test_duration * qps / (
            use_case_metrics_count[usecase] * scale) + 1

    params["timestamp-end"] = generate(timestamp_start + timedelta(seconds=delta_time))
    logging.info(params)

# def getTotalMetrics(params: dict) -> int:
#     return 0
#
# def getTotalRows(params: dict) -> int:
#     return 0
