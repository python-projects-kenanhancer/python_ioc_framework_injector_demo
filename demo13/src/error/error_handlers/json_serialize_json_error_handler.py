import json
import logging

from ..errors import JsonSerializeError
from .error_handler import ErrorHandler


class JsonSerializeJsonErrorHandler(ErrorHandler):
    def handle_error(self, error: JsonSerializeError):
        error_info = {
            "error_type": "JsonSerializationError",
            "message": str(error),
            "detail": error.detail,
        }
        logging.error(json.dumps(error_info))
