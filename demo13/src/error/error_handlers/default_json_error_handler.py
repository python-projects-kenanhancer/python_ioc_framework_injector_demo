import json
import logging

from .error_handler import ErrorHandler


class DefaultJsonErrorHandler(ErrorHandler):
    def handle_error(self, error: Exception):
        error_info = {"error_type": "GeneralError", "message": str(error)}
        logging.error(json.dumps(error_info))
