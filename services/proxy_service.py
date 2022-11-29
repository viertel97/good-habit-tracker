import json
import os
from datetime import datetime

import requests
from loguru import logger

from helper import get_ip
from services.todoist import get_current_offset

logger.add(
    os.path.join(os.path.dirname(os.path.abspath(__file__)) + "/logs/" + os.path.basename(__file__) + ".log"),
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
    backtrace=True,
    diagnose=True,
)


def get_questions(type_of_page):
    return json.loads(requests.get("http://" + get_ip() + ":9000/ght/{type}/".format(type=type_of_page)).json())


SKIP_LIST = ["h1", "h2", "h3", "paragraph"]


def send_inputs(inputs, list_of_entries):
    result_dict = {}
    list_of_entries = [entry for entry in list_of_entries if entry[3] not in SKIP_LIST]
    for idx, entry in enumerate(list_of_entries):
        if entry[3] == "boolean":
            result_dict[entry[0]] = "yes" if inputs[idx] else "no"
        elif entry[3] == "slider":
            if inputs[idx]:
                result_dict[entry[0]] = inputs[idx]
        elif entry[3] == "textarea":
            if inputs[idx] != "" and inputs[idx] is not None:
                result_dict[entry[0]] = inputs[idx]
        else:
            if inputs[idx] == "" or inputs[idx] == None:
                result_dict[entry[0]] = entry[3]
            else:
                result_dict[entry[0]] = inputs[idx]

    result_dict["timestamp"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S" + get_current_offset())
    logger.info(result_dict)
    re = requests.post("http://" + get_ip() + ":9000/ght/", json=result_dict)
    logger.info(re.content)
    return "{code} - {reason} - Thanks!".format(code=re.status_code, reason=re.reason)
