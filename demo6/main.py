import logging
from abc import ABC, abstractmethod

logging.basicConfig(level=logging.INFO)


class DatabaseFetchError(Exception):
    pass


class XmlSerializeError(Exception):
    pass


class EventServiceError(Exception):
    pass


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
        raise DatabaseFetchError("Failed to fetch data from database")


class XmlSerializer(Serializer):
    def serialize(self, data):
        if not data:
            raise XmlSerializeError("XML serialization failed")
        return f"<data><name>{data['name']}</name><email>{data['email']}</email></data>"


class ServiceClient(ABC):
    @abstractmethod
    def call(self, data):
        pass


class EventServiceClient(ServiceClient):
    def call(self, data):
        if not data:
            raise EventServiceError("Failed to connect to service")
        logging.info(f"Calling event service with data: {data}")
        return "<Response><Status>Success</Status></Response>"


class Application:
    def __init__(self, repository: Repository, serializer: Serializer, service_client: ServiceClient):
        self.repository = repository
        self.serializer = serializer
        self.service_client = service_client

    def run(self):
        records = self.repository.find_all()
        serialized_data = self.serializer.serialize(records)
        response = self.service_client.call(serialized_data)
        logging.info(f"Response from service: {response}")


if __name__ == '__main__':
    repository: Repository = DatabaseRepository()
    serializer: Serializer = XmlSerializer()
    service_client: ServiceClient = EventServiceClient()
    app = Application(repository, serializer, service_client)

    try:
        app.run()
    except Exception as ex:
        if isinstance(ex, DatabaseFetchError):
            logging.error(f"Database error occurred: {ex}")
        elif isinstance(ex, XmlSerializeError):
            logging.error(f"Serializer error occurred: {ex}")
        elif isinstance(ex, EventServiceError):
            logging.error(f"Service error occurred: {ex}")
        else:
            logging.error(f"An unexpected error occurred: {ex}")
