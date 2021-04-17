import time

from utils.benchmark_server.metrics import autoset_timestamp_end
from utils.check_criterion import *
from utils.benchmark_server.server import Server
import logging



def workflow_standard(configs):
    logging.info("workflow started...")
    for config in configs:
        invariants = config["invariants"]
        benchmark_server = Server(config["server"])

        for target in config["targets"]:
            params = {}
            params.update(invariants)
            params.update(target)
            if config.get("variant") is not None:
                for val in config["variant"]["values"]:
                    context = {}
                    params.update({config["variant"]["name"]: val})

                    autoset_timestamp_end(params)

                    context["start_time"] = time.time()
                    if not benchmark_server.start(params): return False
                    while True:
                        ok, status = benchmark_server.get_status()
                        if not ok: return False
                        if status == "stopped":
                            break
                        time.sleep(1)
                    context["end_time"] = time.time()

                    if config.get("criterion") is not None:
                        return check_criterion(benchmark_server, config["criterion"], context)
            else:
                context = {}
                context["start_time"] = time.time()
                if not benchmark_server.start(params): return False
                context["end_time"] = time.time()

                if config.get("criterion"):
                    return check_criterion(benchmark_server, config["criterion"], context)

            return True

