import logging
from ..errors import SerializeError


def handle_serialize_error_text(e: SerializeError):
    logging.error(f"Serialization error occurred: {e}. Detail: {e.detail}.")
