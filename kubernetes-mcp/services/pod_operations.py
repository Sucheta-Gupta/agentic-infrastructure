from kubernetes import client 



def list_pods(v1: client.CoreV1Api,namespace: str) -> list:
    pods = v1.list_namespaced_pod(namespace=namespace)

    return [
        {
            "name": pod.metadata.name,
            "namespace": pod.metadata.namespace,
            "status": pod.status.phase,
            "node": pod.spec.node_name,
        }
        for pod in pods.items
    ]


def get_pod_details(v1:client.CoreV1Api,namespace: str,pod_name) -> dict:
    pod = v1.read_namespaced_pod(
        name=pod_name,
        namespace=namespace
    )

    return {
        "name": pod.metadata.name,
        "namespace": pod.metadata.namespace,
        "status": pod.status.phase,
        "node": pod.spec.node_name,
        "pod_ip": pod.status.pod_ip,
        "created_at": str(pod.metadata.creation_timestamp),
    }


def get_nodes(v1:client.CoreV1Api) -> list:
    nodes = v1.list_node()

    return [
        {
            "name": node.metadata.name

        }
        for node in nodes.items
    ]