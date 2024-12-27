import json
import logging

from ..errors import SerializeError


def handle_serialize_error_json(e: SerializeError):
    error_info = {
        "error_type": "SerializationError",
        "message": str(e),
        "detail": e.detail,
    }
    logging.error(json.dumps(error_info))
