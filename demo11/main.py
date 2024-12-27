import logging

from src.application import EventApplication
from src.error import (
    CsvSerializeError,
    DatabaseFetchError,
    ErrorHandlerFactory,
    EventServiceError,
    JsonSerializeError,
    SerializeError,
    XmlSerializeError,
    handle_csv_serialize_error_text,
    handle_database_error_json,
    handle_event_service_error_text,
    handle_general_error_text,
    handle_json_serialize_error_text,
    handle_serialize_error_text,
    handle_xml_serialize_error_text,
)
from src.repositories import DatabaseRepository, Repository
from src.serializers import Serializer, XmlSerializer
from src.services import EventServiceClient, ServiceClient

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    repository: Repository = DatabaseRepository()
    serializer: Serializer = XmlSerializer()
    service_client: ServiceClient = EventServiceClient()

    app = EventApplication(repository, serializer, service_client)

    error_handler_factory = ErrorHandlerFactory()
    error_handler_factory.register_handler(
        DatabaseFetchError, handle_database_error_json
    )
    error_handler_factory.register_handler(SerializeError, handle_serialize_error_text)
    error_handler_factory.register_handler(
        XmlSerializeError, handle_xml_serialize_error_text
    )
    error_handler_factory.register_handler(
        JsonSerializeError, handle_json_serialize_error_text
    )
    error_handler_factory.register_handler(
        CsvSerializeError, handle_csv_serialize_error_text
    )
    error_handler_factory.register_handler(
        EventServiceError, handle_event_service_error_text
    )
    error_handler_factory.register_handler(Exception, handle_general_error_text)

    try:
        app.run()
    except Exception as ex:
        error_handler_factory.handle_error(ex)
