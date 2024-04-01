import logging
from ..errors import EventServiceError


def handle_event_service_error_text(e: EventServiceError):
    logging.error(f"Error calling {e.service_name} service at {e.endpoint}: {e}")
