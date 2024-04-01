import logging
from .service_client import ServiceClient
from ..error.errors import EventServiceError


class EventServiceClient(ServiceClient):
    service_name = "UserEventService"
    endpoint = "/api/events"

    def call(self, data):
        if not data:
            raise EventServiceError("Failed to connect to service", self.service_name, self.endpoint)
        logging.info(f"Calling event service with data: {data}")
        return "<Response><Status>Success</Status></Response>"
