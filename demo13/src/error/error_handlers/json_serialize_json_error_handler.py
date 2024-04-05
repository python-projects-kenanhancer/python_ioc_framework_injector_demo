import logging
import json
from .error_handler import ErrorHandler
from ..errors import JsonSerializeError


class JsonSerializeJsonErrorHandler(ErrorHandler):
    def handle_error(self, error: JsonSerializeError):
        error_info = {
            "error_type": "JsonSerializationError",
            "message": str(error),
            "detail": error.detail,
        }
        logging.error(json.dumps(error_info))
