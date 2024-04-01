from abc import ABC, abstractmethod


class Repository(ABC):
    @abstractmethod
    def find_all(self):
        pass
