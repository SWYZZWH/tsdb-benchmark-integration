from utils.workflow import workflow_standard


def test_batchsize(batchsize_configs, docker_client):
    assert workflow_standard(batchsize_configs, docker_client)


