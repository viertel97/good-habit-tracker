from quarter_lib.logging import setup_logging

from services.html_service import generate_layout_html

logger = setup_logging(__file__)


def generate_layout():
    return generate_layout_html()
