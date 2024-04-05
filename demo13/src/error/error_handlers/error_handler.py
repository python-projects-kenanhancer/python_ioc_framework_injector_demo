from abc import ABC, abstractmethod


class ErrorHandler(ABC):
    @abstractmethod
    def handle_error(self, error: Exception):
        pass
