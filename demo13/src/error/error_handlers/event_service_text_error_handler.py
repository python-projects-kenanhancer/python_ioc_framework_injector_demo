import logging

from ..errors import EventServiceError
from .error_handler import ErrorHandler


class EventServiceTextErrorHandler(ErrorHandler):
    def handle_error(self, error: EventServiceError):
        logging.error(
            f"Error calling {error.service_name} service at {error.endpoint}: {error}"
        )
