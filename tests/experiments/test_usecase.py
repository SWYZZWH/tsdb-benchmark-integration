from utils.workflow import workflow_standard


def test_usecase(usecase_configs, docker_client):
    assert workflow_standard(usecase_configs, docker_client)


