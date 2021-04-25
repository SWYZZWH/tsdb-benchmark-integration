from utils.workflow import workflow_standard


def test_worker(test_configs, docker_client):
    assert workflow_standard(test_configs, docker_client)


