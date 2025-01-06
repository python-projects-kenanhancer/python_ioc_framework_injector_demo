from abc import ABC, abstractmethod


class GreetingStrategy(ABC):
    @abstractmethod
    def get_greeting_prefix(self, name: str) -> str:
        raise NotImplementedError
