import time
import logging
from functools import reduce

import docker
from docker import DockerClient
import json
from definitions import *

docker_images_map = {
    INFLUX: {"image": "influxdb:1.8", "params": {"ports": {"8086": "8086"}}},
    VICTORIA_METRICS: {"image": "victoriametrics/victoria-metrics:v1.58.0", "params": {"ports": {"8428": "8428"}}},
    TIMESCALEDB: {"image": "timescale/timescaledb:2.0.0-pg12",
                  "params": {"ports": {"5432": "5432"}, "environment": ["POSTGRES_PASSWORD=password"]}
                  }
}


def delete_all_containers(client: DockerClient):
    stop_all_containers(client)
    client.containers.prune()


def stop_all_containers(client: DockerClient) -> bool:
    container_list = client.containers.list()
    for container in container_list:
        stop_container(container)

    time.sleep(5)

    return len(client.containers.list()) == 0


def start_container(client: DockerClient, target):
    if target not in docker_images_map.keys():
        logging.log("unsupported target:{}".format(target))
        assert False

    # ensure no other containers is running
    assert len(client.containers.list()) == 0

    # check the images
    image = docker_images_map[target]
    container = client.containers.run(image=image["image"], command="", detach=True, **image["params"])

    assert container is not None

    time.sleep(5)
    return container


def stop_container(container):
    logging.info("close_container {}, {}".format(container.id, container.stop()))


class StatsAgent:  # one agent for one container

    def __init__(self, base_url, container_id=None):
        self.client = docker.api.APIClient(base_url=base_url)
        self.container_id = container_id
        self.stats_generator = self.client.stats(container=container_id) if container_id is not None else None
        next(self.stats_generator)  # get initial state

        self.stats = {}

    def _parse_response(self, res) -> dict:
        res = json.loads(res)
        cpu_stats = res["cpu_stats"]
        precpu_stats = res["precpu_stats"]
        cpu_delta = cpu_stats["cpu_usage"]["total_usage"] - precpu_stats["cpu_usage"]["total_usage"]
        system_cpu_delta = cpu_stats["system_cpu_usage"] - precpu_stats["system_cpu_usage"]
        number_cpus = cpu_stats["online_cpus"]
        cpu_usage = (cpu_delta / system_cpu_delta) * number_cpus * 100.0
        memory_stats = res["memory_stats"]
        memory_usage = memory_stats["usage"] / (1024 * 1024 * 1024)  # unit MB
        return {"cpu_usage": round(cpu_usage, 3), "memory_usage": round(memory_usage, 3)}

    def fetch_stats(self, container_id=None):
        if self.container_id is None and container_id is None:
            logging.error("please give the container id")
            return
        if self.container_id is not None and container_id is not None and self.container_id != container_id:
            logging.error("use correct container id: {}".format(self.container_id))
            return

        if self.container_id is None:
            self.container_id = container_id
        if self.stats_generator is None:
            self.stats_generator = self.client.stats(container=container_id)
            next(self.stats_generator)

        response = next(self.stats_generator)

        if "cpu_usage" not in self.stats.keys():
            self.stats["cpu_usage"] = []
        if "memory_usage" not in self.stats.keys():
            self.stats["memory_usage"] = []

        self.stats["cpu_usage"].append((self._parse_response(response))["cpu_usage"])
        self.stats["memory_usage"].append((self._parse_response(response))["memory_usage"])

    def all_stats(self) -> dict:
        if len(self.stats) == 0:
            return {}

        return self.stats

    def summary(self) -> dict:
        if len(self.stats) == 0:
            return {}

        cpu_usage = sum([stat["cpu_usage"] for stat in self.stats]) / len([stat["cpu_usage"] for stat in self.stats])
        memory_usage = sum([stat["memory_usage"] for stat in self.stats]) / len(
            [stat["memory_usage"] for stat in self.stats])

        return {"cpu_usage": cpu_usage, "memory_usage": memory_usage}


def test_statsagent():
    client = docker.from_env()
    id = client.containers.list()[0].id
    sa = StatsAgent("http://localhost:2375", id)
    for i in range(10):
        sa.fetch_stats(id)
        time.sleep(1)
    print(sa.all_stats())


def test_startcontainer():
    client = docker.from_env()
    stop_all_containers(client)

    start_container(client, "influx")
    assert len(client.containers.list()) == 1


if __name__ == "__main__":
    test_startcontainer()
    test_statsagent()
