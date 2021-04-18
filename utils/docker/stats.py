import docker


def get_stats(client: docker.api.APIClient, container_id):
    stats = client.stats(container=container_id)
    cpu_usage = 0
    memory_usage = 0
