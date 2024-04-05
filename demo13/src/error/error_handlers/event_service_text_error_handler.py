import logging
from .error_handler import ErrorHandler
from ..errors import EventServiceError


class EventServiceTextErrorHandler(ErrorHandler):
    def handle_error(self, error: EventServiceError):
        logging.error(f"Error calling {error.service_name} service at {error.endpoint}: {error}")
