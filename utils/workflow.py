import time

from definitions import BASE_URL
from utils.benchmark_server.metrics import autoset_timestamp_end
from utils.check_criterion import *
from utils.benchmark_server.server import Server
import logging
import os
from utils.docker.containers import start_container, stop_container, stop_all_containers, StatsAgent, \
    delete_all_containers
from utils.report.report import Report, Result


def workflow_standard(configs, docker_client):
    logging.info("workflow started...")
    for config in configs:
        invariants = config["invariants"]
        benchmark_server = Server(config["server"])

        report = Report(title=config["variant"]["name"], variant=config["variant"]["name"])
        for target in config["targets"]:
            params = {}
            params.update(invariants)
            params.update(target)
            is_valid = True

            for val in config["variant"]["values"]:
                delete_all_containers(docker_client)
                container = start_container(docker_client, target["db"])  # start this target
                stats_agent = StatsAgent(BASE_URL, container.id)

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
                    is_valid = check_criterion(benchmark_server, target["db"], config, context)

                # get statistics
                report.add_result(Result(target["db"], val, stats_agent.all_stats()), is_valid)
                stop_container(container)

        report.generate_report(os.getcwd())
        return True

