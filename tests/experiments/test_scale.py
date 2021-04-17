from utils.workflow import workflow_standard


def test_scale(scale_configs):
    assert workflow_standard(scale_configs)
