import json
import logging

from ..errors import DatabaseFetchError
from .error_handler import ErrorHandler


class DatabaseJsonErrorHandler(ErrorHandler):
    def handle_error(self, error: DatabaseFetchError):
        error_info = {
            "error_type": "DatabaseError",
            "message": str(error),
            "error_code": error.error_code,
            "query": error.query,
        }
        logging.error(json.dumps(error_info))
