from abc import ABC, abstractmethod
from enum import Enum

from injector import Binder, Injector, Module, inject, singleton


class GreetingStrategy(ABC):
    @abstractmethod
    def get_greeting_prefix(self, name: str) -> str:
        raise NotImplementedError


class BasicGreetingStrategy(GreetingStrategy):
    def get_greeting_prefix(self, name: str) -> str:
        return f"Hello, {name}!"


class HolidayGreetingStrategy(GreetingStrategy):
    def get_greeting_prefix(self, name: str) -> str:
        return f"Happy Holidays, {name}!"


class TimeBasedGreetingStrategy(GreetingStrategy):
    def get_greeting_prefix(self, name: str) -> str:
        return f"Good day, {name}!"


class GreetingType(Enum):
    HOLIDAY = HolidayGreetingStrategy
    TIME_BASED = TimeBasedGreetingStrategy
    BASIC = BasicGreetingStrategy


class AppConfig:
    def __init__(
        self,
        database_url: str,
        enable_feature_x: bool,
        enable_feature_y: bool,
        greeting_strategy: GreetingType,
    ):
        self.database_url = database_url
        self.enable_feature_x = enable_feature_x
        self.enable_feature_y = enable_feature_y
        self.greeting_strategy = greeting_strategy


class GreetingService:
    @inject
    def __init__(self, app_config: AppConfig, injector: Injector):
        self._app_config = app_config
        self._injector = injector

    def greet(self, name: str) -> str:
        strategy_enum = self._app_config.greeting_strategy
        greeting_strategy = self._injector.get(strategy_enum.value)
        return greeting_strategy.get_greeting_prefix(name)


class ConfigModule(Module):
    def __init__(self, config: AppConfig):
        self.config = config

    def configure(self, binder: Binder) -> None:
        binder.bind(AppConfig, self.config, scope=singleton)


class GreetingModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(
            GreetingType.HOLIDAY.value, to=HolidayGreetingStrategy, scope=singleton
        )
        binder.bind(
            GreetingType.TIME_BASED.value, to=TimeBasedGreetingStrategy, scope=singleton
        )
        binder.bind(GreetingType.BASIC.value, to=BasicGreetingStrategy, scope=singleton)


if __name__ == "__main__":
    config = AppConfig(
        database_url="mysql://localhost:3306/mydb",
        enable_feature_x=True,
        enable_feature_y=False,
        greeting_strategy=GreetingType.HOLIDAY,
    )

    injector = Injector([GreetingModule, ConfigModule(config)])

    app_config = injector.get(AppConfig)

    print(app_config)

    greeting_strategy = injector.get(GreetingType.HOLIDAY.value)

    print(greeting_strategy)

    greeting_service = injector.get(GreetingService)

    print(greeting_service.greet("Kenan"))
