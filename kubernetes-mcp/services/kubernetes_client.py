from kubernetes import config, client 


def initialize_client():
    config.load_kube_config()


    v1 = client.CoreV1Api()
    return v1