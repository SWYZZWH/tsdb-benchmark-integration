import time

from definitions import BASE_URL
from utils.benchmark_server.metrics import autoset_timestamp_end
from utils.check_criterion import *
from utils.benchmark_server.server import Server
import logging
import os
from utils.docker.containers import start_container, stop_container, stop_all_containers, StatsAgent
from utils.report.report import Report, Result


def workflow_standard(configs, docker_client):
    logging.info("workflow started...")
    for config in configs:
        invariants = config["invariants"]
        benchmark_server = Server(config["server"])

        report = Report(title=config["variant"]["name"], variant=config["variant"]["name"])
        for target in config["targets"]:
            stop_all_containers(docker_client)
            container = start_container(docker_client, target["db"])  # start this target
            stats_agent = StatsAgent(BASE_URL, container.id)

            params = {}
            params.update(invariants)
            params.update(target)

            for val in config["variant"]["values"]:
                context = {}
                params.update({config["variant"]["name"]: val})

                autoset_timestamp_end(params)

                context["start_time"] = time.time()
                if not benchmark_server.start(params): return False
                while True:
                    ok, status = benchmark_server.get_status()
                    if not ok:
                        return False
                    if status == "stopped":
                        break
                    stats_agent.fetch_stats()
                    time.sleep(1)
                context["end_time"] = time.time()

                if config.get("criterion") is not None:
                    return check_criterion(benchmark_server, config["criterion"], context)

                # get statistics
                report.add_result(Result(target["db"], val, stats_agent.summary()))

            stop_container(container)

        report.print_pics(os.getcwd())
        return True

