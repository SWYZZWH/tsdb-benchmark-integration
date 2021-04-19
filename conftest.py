import pytest
import yaml
import logging
import docker
from utils.check_config import *


@pytest.fixture
def yaml_loader():
    def _yaml_loader(file):
        with open(file, "r") as f:
            try:
                return yaml.load(f.read(), Loader=yaml.FullLoader)
            except Exception as e:
                logging.error(e)
                return None

    yield _yaml_loader


@pytest.fixture
def config_loader(yaml_loader):
    def _config_loader(file):
        config = yaml_loader(file)
        assert check_config(config)
        return config

    yield _config_loader

@pytest.fixture
def docker_client():
    return docker.from_env()


