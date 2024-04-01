import json
import logging
from ..errors import EventServiceError


def handle_event_service_error_json(e: EventServiceError):
    error_info = {
        "error_type": "EventServiceError",
        "message": str(e),
        "service_name": e.service_name,
        "endpoint": e.endpoint
    }
    logging.error(json.dumps(error_info))
