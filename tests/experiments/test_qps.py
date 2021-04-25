from utils.workflow import workflow_standard


def test_qps(qps_configs, docker_client):
    assert workflow_standard(qps_configs, docker_client)


