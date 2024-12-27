import json
import logging

from ..errors import EventServiceError
from .error_handler import ErrorHandler


class EventServiceJsonErrorHandler(ErrorHandler):
    def handle_error(self, error: EventServiceError):
        error_info = {
            "error_type": "EventServiceError",
            "message": str(error),
            "service_name": error.service_name,
            "endpoint": error.endpoint,
        }
        logging.error(json.dumps(error_info))
