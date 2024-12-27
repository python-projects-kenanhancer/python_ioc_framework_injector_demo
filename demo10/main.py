import json
import logging
from abc import ABC, abstractmethod

logging.basicConfig(level=logging.INFO)


class DatabaseFetchError(Exception):
    def __init__(self, message="", error_code=None, query=""):
        super().__init__(message)
        self.error_code = error_code
        self.query = query


class XmlSerializeError(Exception):
    def __init__(self, message="", detail="", element=""):
        super().__init__(message)
        self.detail = detail
        self.element = element


class EventServiceError(Exception):
    def __init__(self, message="", service_name="", endpoint=""):
        super().__init__(message)
        self.service_name = service_name
        self.endpoint = endpoint


class Repository(ABC):
    @abstractmethod
    def find_all(self):
        pass


class Serializer(ABC):
    @abstractmethod
    def serialize(self, data):
        pass


class DatabaseRepository(Repository):
    def find_all(self):
        # return {"name": "John Doe", "email": "john@example.com"}
        raise DatabaseFetchError(
            "Failed to fetch data from database", 5001, "SELECT * FROM users"
        )


class XmlSerializer(Serializer):
    element = "<user>"

    def serialize(self, data):
        if not data:
            raise XmlSerializeError(
                "XML serialization failed", "Missing closing tag", self.element
            )
        return f"<data><name>{data['name']}</name><email>{data['email']}</email></data>"


class ServiceClient(ABC):
    @abstractmethod
    def call(self, data):
        pass


class EventServiceClient(ServiceClient):
    service_name = "UserEventService"
    endpoint = "/api/events"

    def call(self, data):
        if not data:
            raise EventServiceError(
                "Failed to connect to service", self.service_name, self.endpoint
            )
        logging.info(f"Calling event service with data: {data}")
        return "<Response><Status>Success</Status></Response>"


def handle_database_error_text(e: DatabaseFetchError):
    logging.error(
        f"Database error occurred: {e}. Error code: {e.error_code}. Query: {e.query}"
    )


def handle_serialize_error_text(e: XmlSerializeError):
    logging.error(
        f"Serialization error occurred: {e}. Detail: {e.detail}. Element: {e.element}"
    )


def handle_event_service_error_text(e: EventServiceError):
    logging.error(f"Error calling {e.service_name} service at {e.endpoint}: {e}")


def handle_general_error_text(e: Exception):
    logging.error(f"An unexpected error occurred: {e}")


def handle_database_error_json(e: DatabaseFetchError):
    error_info = {
        "error_type": "DatabaseError",
        "message": str(e),
        "error_code": e.error_code,
        "query": e.query,
    }
    logging.error(json.dumps(error_info))


def handle_serialize_error_json(e: XmlSerializeError):
    error_info = {
        "error_type": "SerializationError",
        "message": str(e),
        "detail": e.detail,
        "element": e.element,
    }
    logging.error(json.dumps(error_info))


def handle_event_service_error_json(e: EventServiceError):
    error_info = {
        "error_type": "EventServiceError",
        "message": str(e),
        "service_name": e.service_name,
        "endpoint": e.endpoint,
    }
    logging.error(json.dumps(error_info))


def handle_general_error_json(e: Exception):
    error_info = {"error_type": "GeneralError", "message": str(e)}
    logging.error(json.dumps(error_info))


class Application:
    def __init__(
        self,
        repository: Repository,
        serializer: Serializer,
        service_client: ServiceClient,
    ):
        self.repository = repository
        self.serializer = serializer
        self.service_client = service_client

    def run(self):
        records = self.repository.find_all()
        serialized_data = self.serializer.serialize(records)
        response = self.service_client.call(serialized_data)
        logging.info(f"Response from service: {response}")


if __name__ == "__main__":
    repository: Repository = DatabaseRepository()
    serializer: Serializer = XmlSerializer()
    service_client: ServiceClient = EventServiceClient()
    error_handlers = {
        DatabaseFetchError: handle_database_error_json,
        XmlSerializeError: handle_serialize_error_text,
        EventServiceError: handle_event_service_error_text,
        Exception: handle_general_error_text,  # General errors handler
    }
    app = Application(repository, serializer, service_client)

    try:
        app.run()
    except Exception as ex:
        error_handler = error_handlers.get(type(ex), error_handlers.get(Exception))
        if error_handler:
            error_handler(ex)
        else:
            logging.error(f"No handler for error: {ex}")
