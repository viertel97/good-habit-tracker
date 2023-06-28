import os


def get_ip():
    # return "localhost" if get_debug() else "0.0.0.0"
    return "localhost" if not os.name == "nt" else "192.168.178.100"


def get_debug():
    return True if os.name == "nt" else False
