import logging
from abc import ABC, abstractmethod

logging.basicConfig(level=logging.INFO)


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
        return {"name": "John Doe", "email": "john@example.com"}


class XmlSerializer(Serializer):
    def serialize(self, data):
        return f"<data><name>{data['name']}</name><email>{data['email']}</email></data>"


class ServiceClient(ABC):
    @abstractmethod
    def call(self, data):
        pass


class EventServiceClient(ServiceClient):
    def call(self, data):
        logging.info(f"Calling event service with data: {data}")
        # return xml response
        return "<Response><Status>Success</Status></Response>"


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
    repository = DatabaseRepository()
    serializer = XmlSerializer()
    service_client = EventServiceClient()
    app = Application(repository, serializer, service_client)

    try:
        app.run()
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
