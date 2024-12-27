import logging

from src.application import EventApplication
from src.error import configure_error_handlers
from src.repositories import DatabaseRepository, Repository
from src.serializers import Serializer, XmlSerializer
from src.services import EventServiceClient, ServiceClient

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    repository: Repository = DatabaseRepository()
    serializer: Serializer = XmlSerializer()
    service_client: ServiceClient = EventServiceClient()

    app = EventApplication(repository, serializer, service_client)

    error_handler_factory = configure_error_handlers()

    try:
        app.run()
    except Exception as ex:
        error_handler_factory.handle_error(ex)
