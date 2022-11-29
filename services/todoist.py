import os

import requests
from loguru import logger

logger.add(
    os.path.join(os.path.dirname(os.path.abspath(__file__)) + "/logs/" + os.path.basename(__file__) + ".log"),
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
    backtrace=True,
    diagnose=True,
)
headers = {"Authorization": f"Bearer {os.environ['TODOIST_TOKEN']}"}


def get_current_offset():
    return requests.post(
        "https://api.todoist.com/sync/v9/sync",
        headers={
            "Authorization": f"Bearer {os.environ['TODOIST_TOKEN']}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={"sync_token": "*", "resource_types": '["user"]'},
    ).json()["user"]["tz_info"]["gmt_string"]
