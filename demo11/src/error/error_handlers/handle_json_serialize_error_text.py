import logging

from ..errors import JsonSerializeError


def handle_json_serialize_error_text(e: JsonSerializeError):
    logging.error(f"JSON Serialization error occurred: {e}. Detail: {e.detail}.")
