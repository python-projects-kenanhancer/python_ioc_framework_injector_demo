import logging
from ..repositories import Repository
from ..serializers import Serializer
from ..services import ServiceClient


class EventApplication:
    def __init__(self, repository: Repository, serializer: Serializer, service_client: ServiceClient):
        self.repository = repository
        self.serializer = serializer
        self.service_client = service_client

    def run(self):
        records = self.repository.find_all()
        serialized_data = self.serializer.serialize(records)
        response = self.service_client.call(serialized_data)
        logging.info(f"Response from service: {response}")
