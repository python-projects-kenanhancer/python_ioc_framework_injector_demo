from abc import ABC, abstractmethod


class ServiceClient(ABC):
    @abstractmethod
    def call(self, data):
        pass
