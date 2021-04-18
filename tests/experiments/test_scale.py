from utils.workflow import workflow_standard


def test_scale(scale_configs, docker_client):
    assert workflow_standard(scale_configs, docker_client)
