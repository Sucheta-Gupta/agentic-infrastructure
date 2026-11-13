from mcp.server import MCPServer
from services.pod_operations import (list_pods , 
                                     get_pod_details as fetch_pod_details,
                                     get_nodes as fetch_nodes )
from services.kubernetes_client import initialize_client


mcp = MCPServer("kubernetes-mcp")
v1 = initialize_client()

@mcp.tool()
def get_pods(namespace: str) -> list:
    """list all pods in a kubernetes namespace"""

    return list_pods(v1,namespace)

@mcp.tool()
def get_pod_details(namespace: str,pod_name: str)  -> dict:
    """Get details of pods"""

    return fetch_pod_details(v1,namespace,pod_name)


@mcp.tool()
def get_nodes()  -> list:
    """Get details of nodes"""

    return fetch_nodes(v1)

if __name__=="__main__":
    mcp.run(
        transport="streamable-http",
        host="127.0.0.1",
        port=8000,

    )