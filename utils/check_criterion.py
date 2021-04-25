from utils.targets.influx import Influx
from utils.targets.timescaledb import Timescaledb
from utils.targets.victoriametrics import Victoriametrics
import logging

def parseTarget(db):
    target = None
    if db == "influx":
        target = Influx
    elif db == "victoriametrics":
        target = Victoriametrics
    elif db == "timescaledb":
        target = Timescaledb
    return target


def check_time_deviation_rate(expected_time, real_time, rate):
    # if user set expected_time is 100 second, however it costs 200 seconds to finish one test,
    # it means the real qps is less than what user sets, so the test is invalid
    time_deviation_rate = abs(float(real_time) - float(expected_time)) / float(expected_time)
    if time_deviation_rate < rate:
        return True
    else:
        logging.error("time deviation is {}, larger than {}".format(time_deviation_rate, rate))
        return False


def check_metrics_missing_rate(server, db, context, total_sent_metrics, rate):
    target = parseTarget(db)
    total_received_metrics = target.query_total_metrics(context["start_time"], context["end_time"])
    print(total_sent_metrics, total_received_metrics)
    return (total_sent_metrics - total_received_metrics) >= 0 and \
           (total_sent_metrics - total_received_metrics) / total_sent_metrics < float(rate)


def check_criterion(server, db, config, context) -> bool:
    ok, report_map = server.get_report()
    assert ok
    expected_time = config["invariants"]["expected-test-duration"]
    criterion = config["criterion"]

    if "max-metrics-missing-rate" in criterion.keys():
        if not check_metrics_missing_rate(server, db, context, report_map["total_metrics"],
                                          criterion["max-metrics-missing-rate"]):
            return False

    if "max-time-deviation-rate" in criterion.keys():
        if not check_time_deviation_rate(expected_time, report_map["total_time"], criterion["max-time-deviation-rate"]):
            return False

    return True
