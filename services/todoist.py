import os
from quarter_lib.akeyless import get_secrets
import requests
from quarter_lib.logging import setup_logging

TODOIST_TOKEN = get_secrets(["todoist/token"])

logger = setup_logging(__file__)
headers = {"Authorization": f"Bearer {TODOIST_TOKEN}"}


def get_current_offset():
    return requests.post(
        "https://api.todoist.com/sync/v9/sync",
        headers={
            "Authorization": f"Bearer {TODOIST_TOKEN}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={"sync_token": "*", "resource_types": '["user"]'},
    ).json()["user"]["tz_info"]["gmt_string"]
