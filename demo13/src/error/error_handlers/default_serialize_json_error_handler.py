import json
import logging
from .error_handler import ErrorHandler
from ..errors import SerializeError


class DefaultSerializeJsonErrorHandler(ErrorHandler):
    def handle_error(self, error: SerializeError):
        error_info = {
            "error_type": "SerializationError",
            "message": str(error),
            "detail": error.detail,
        }
        logging.error(json.dumps(error_info))
