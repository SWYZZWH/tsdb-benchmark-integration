import time
import logging
import docker
from docker import DockerClient

from definitions import *

docker_images_map = {
    INFLUX: {"image": "influxdb:1.8", "command": "-p 8086:8086 -d"},
    VICTORIA_METRICS: {"image": "victoriametrics/victoria-metrics:v1.58.0",
                       "command": "-d --name timescaledb -p 5432:5432 -e POSTGRES_PASSWORD=password"},
    TIMESCALEDB: {"image": "timescale/timescaledb:2.0.0-pg12", "command": "-p 8428:8428 -d"}
}


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
    container = client.containers.run(image=image["mage"], command=image["command"], detach=True)
    assert container is not None

    return container


def stop_container(container):
    logging.info("close_container {}, {}".format(container.id, container.stop(container.id)))
