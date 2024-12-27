import json
import logging

from ..errors import SerializeError
from .error_handler import ErrorHandler


class DefaultSerializeJsonErrorHandler(ErrorHandler):
    def handle_error(self, error: SerializeError):
        error_info = {
            "error_type": "SerializationError",
            "message": str(error),
            "detail": error.detail,
        }
        logging.error(json.dumps(error_info))
