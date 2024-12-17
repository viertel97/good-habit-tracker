import os
from platform import platform

from quarter_lib.logging import setup_logging

DEBUG = platform == "darwin" or platform == "win32" or platform == "Windows"
IS_CONTAINER = os.environ.get("IS_CONTAINER", "False") == "True"

logger = setup_logging(__file__)


if IS_CONTAINER:
    IP = "tasker-proxy.custom.svc.cluster.local"
else:
    IP = "localhost"
logger.info("IP: " + IP)


def get_ip():
    return IP + ":9000"


def get_debug():
    return True if os.name == "nt" else False


def get_url(service):
    if DEBUG:
        return "http://192.168.178.49:9300"
    else:
        return f"http://{service}.custom.svc.cluster.local:80"
