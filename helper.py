import os

IS_CONTAINER = os.environ.get("IS_CONTAINER", "False") == "True"


def get_ip():
    if IS_CONTAINER:
        return "tasker-proxy.default.svc.cluster.local"
    else:
        return "localhost:9000"  # if not os.name == "nt" else "localhost"


def get_debug():
    return True if os.name == "nt" else False
