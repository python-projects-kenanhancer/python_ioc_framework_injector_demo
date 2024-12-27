import json
import logging

from ..errors import JsonSerializeError


def handle_json_serialize_error_json(e: JsonSerializeError):
    error_info = {
        "error_type": "JsonSerializationError",
        "message": str(e),
        "detail": e.detail,
    }
    logging.error(json.dumps(error_info))
