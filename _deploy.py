import os
import sys

sys.path.append("..")

import glob

from loguru import logger
from quarter_lib.deployment import deploy_to_server_with_folders

logger.add(
    os.path.join(os.path.dirname(os.path.abspath(__file__)) + "/logs/" + os.path.basename(__file__) + ".log"),
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
    backtrace=True,
    diagnose=True,
)


APPLICATION_NAME = "GHT"
APPLICATION_PATH = "GHT"


if __name__ == "__main__":
    files = glob.glob("**/*.py", recursive=True)
    files.extend(glob.glob("**/*.css", recursive=True))
    files.remove(os.path.basename(__file__))
    files = [file for file in files if not file.endswith("__init__.py") and not file.startswith("venv")]
    files.extend(["requirements.txt", "requirements_custom.txt", "process.json"])
    deploy_to_server_with_folders(
        root_path=os.path.dirname(os.path.abspath(__file__)),
        files=files,
        application_path=APPLICATION_PATH,
        application_name=APPLICATION_NAME,
    )
    print("done")
