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
    url = "http://" + get_ip() + "/ght/" + type_of_page
    logger.info("Getting questions from: " + url)
    response = requests.get(url)
    return response.json()


SKIP_LIST = ["h1", "h2", "h3", "paragraph"]


def send_inputs(inputs, list_of_entries):
    result_dict = {}
    list_of_entries = [entry for entry in list_of_entries if entry['default_type'] not in SKIP_LIST]
    for idx, entry in enumerate(list_of_entries):
        selected_value = inputs[idx]
        if entry['default_type'] == "boolean":
            result_dict[entry['code']] = "yes" if selected_value else "no"
        elif entry['default_type'] == "slider":
            if selected_value:
                result_dict[entry['code']] = selected_value
        elif entry['default_type'] == "textarea":
            if selected_value != "" and selected_value is not None:
                result_dict[entry['code']] = selected_value
        else:
            if selected_value == "" or selected_value == None:
                result_dict[entry['code']] = entry['default_type']
            else:
                result_dict[entry['code']] = selected_value

    result_dict["timestamp"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S" + get_current_offset())
    logger.info(result_dict)
    re = requests.post("http://" + get_ip() + "/ght/", json=result_dict)
    logger.info(re.content)
    return "{code} - {reason} - Thanks!".format(code=re.status_code, reason=re.reason)
