import json
import logging
from .error_handler import ErrorHandler
from ..errors import EventServiceError


class EventServiceJsonErrorHandler(ErrorHandler):
    def handle_error(self, error: EventServiceError):
        error_info = {
            "error_type": "EventServiceError",
            "message": str(error),
            "service_name": error.service_name,
            "endpoint": error.endpoint
        }
        logging.error(json.dumps(error_info))
