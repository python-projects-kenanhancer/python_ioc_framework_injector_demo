import json
import logging
from .error_handler import ErrorHandler
from ..errors import CsvSerializeError


class CsvSerializeJsonErrorHandler(ErrorHandler):
    def handle_error(self, error: CsvSerializeError):
        error_info = {
            "error_type": "CsvSerializationError",
            "message": str(error),
            "detail": error.detail,
        }
        logging.error(json.dumps(error_info))
