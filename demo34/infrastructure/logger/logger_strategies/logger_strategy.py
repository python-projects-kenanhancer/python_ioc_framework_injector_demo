from abc import ABC, abstractmethod


class LoggerStrategy(ABC):
    @abstractmethod
    def info(self, msg: str, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def warning(self, msg: str, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def error(self, msg: str, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def debug(self, msg, *args, **kwargs) -> None:
        pass
