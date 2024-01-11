import os
from quarter_lib.logging import setup_logging

logger = setup_logging(__file__)

IS_CONTAINER = os.environ.get("IS_CONTAINER", "False") == "True"

if IS_CONTAINER:
    IP = "tasker-proxy.custom.svc.cluster.local"
else:
    IP = "localhost"
logger.info("IP: " + IP)


def get_ip():
    return IP + ":9000"


def get_debug():
    return True if os.name == "nt" else False
