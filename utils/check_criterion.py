from utils.gateway.query import query_total_metrics


def check_criterion(server, criterion, context) -> bool:
    if "max-metrics-missing-rate" in criterion.keys():
        rate = criterion["max-metrics-missing-rate"]
        ok, report_map = server.get_report()
        assert ok

        total_sent_metrics = report_map["total_metrics"]
        total_received_metrics = query_total_metrics(context["start_time"], context["end_time"])
        print(total_sent_metrics, total_received_metrics)
        if not (total_sent_metrics - total_received_metrics) >= 0 and \
                (total_sent_metrics - total_received_metrics) / total_sent_metrics < float(rate):
            return False

    return True