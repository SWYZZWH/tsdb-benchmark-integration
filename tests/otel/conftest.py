import pytest
import definitions
import os


@pytest.fixture
def missing_points_configs(config_loader) -> list:
    config_file_path = os.path.join(os.path.join(definitions.CONFIG_DIR, "otel"), "missing_points.yaml")
    print(config_file_path)
    configs = [config_loader(config_file_path)]
    print(configs)
    yield configs
