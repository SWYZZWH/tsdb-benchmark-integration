from utils.workflow import workflow_standard


def test_worker(worker_configs, docker_client):
    assert workflow_standard(worker_configs, docker_client)


