import pytest
import definitions
import os


@pytest.fixture
def scale_configs(config_loader) -> list:
    config_file_path = os.path.join(os.path.join(definitions.CONFIG_DIR, "experiments"), "test_scale.yaml")
    print(config_file_path)
    configs = [config_loader(config_file_path)]
    print(configs)
    yield configs


@pytest.fixture
def batchsize_configs(config_loader) -> list:
    config_file_path = os.path.join(os.path.join(definitions.CONFIG_DIR, "experiments"), "test_batchsize.yaml")
    print(config_file_path)
    configs = [config_loader(config_file_path)]
    print(configs)
    yield configs

@pytest.fixture
def usecase_configs(config_loader) -> list:
    config_file_path = os.path.join(os.path.join(definitions.CONFIG_DIR, "experiments"), "test_usecase.yaml")
    print(config_file_path)
    configs = [config_loader(config_file_path)]
    print(configs)
    yield configs

@pytest.fixture
def qps_configs(config_loader) -> list:
    config_file_path = os.path.join(os.path.join(definitions.CONFIG_DIR, "experiments"), "test_qps.yaml")
    print(config_file_path)
    configs = [config_loader(config_file_path)]
    print(configs)
    yield configs

@pytest.fixture
def worker_configs(config_loader) -> list:
    config_file_path = os.path.join(os.path.join(definitions.CONFIG_DIR, "experiments"), "test_worker.yaml")
    print(config_file_path)
    configs = [config_loader(config_file_path)]
    print(configs)
    yield configs

@pytest.fixture
def test_configs(config_loader) -> list:
    config_file_path = os.path.join(os.path.join(definitions.CONFIG_DIR, "experiments"), "test_test.yaml")
    print(config_file_path)
    configs = [config_loader(config_file_path)]
    print(configs)
    yield configs