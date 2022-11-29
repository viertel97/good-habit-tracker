import os
from pathlib import Path

from loguru import logger
from services.html_service import generate_layout_html

logger.add(
    os.path.join(os.path.dirname(os.path.abspath(__file__)) + "/logs/" + os.path.basename(__file__) + ".log"),
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
    backtrace=True,
    diagnose=True,
)


def generate_layout():
    return generate_layout_html()
