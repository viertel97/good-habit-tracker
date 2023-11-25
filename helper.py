import os


def get_ip():
    # return "localhost" if get_debug() else "0.0.0.0"
    return "localhost" # if not os.name == "nt" else "localhost"


def get_debug():
    return True if os.name == "nt" else False
