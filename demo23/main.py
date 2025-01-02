from enum import Enum
from typing import NewType

from injector import Binder, Injector, Module, singleton

holiday = NewType("holiday", str)
time_based = NewType("time_based", str)
basic = NewType("basic", str)


class GreetingType(Enum):
    HOLIDAY = holiday
    TIME_BASED = time_based
    BASIC = basic


class HolidayGreeting:
    pass


class TimeBasedGreeting:
    pass


class BasicGreeting:
    pass


class AppConfig:
    def __init__(
        self, database_url: str, enable_feature_x: bool, enable_feature_y: bool
    ):
        self.database_url = database_url
        self.enable_feature_x = enable_feature_x
        self.enable_feature_y = enable_feature_y


class GreetingModule(Module):
    def __init__(self, config: AppConfig):
        self.config = config

    def configure(self, binder: Binder) -> None:
        binder.bind(GreetingType.HOLIDAY.value, to=HolidayGreeting, scope=singleton)
        binder.bind(
            GreetingType.TIME_BASED.value, to=TimeBasedGreeting, scope=singleton
        )
        binder.bind(GreetingType.BASIC.value, to=BasicGreeting, scope=singleton)
        binder.bind(AppConfig, self.config, scope=singleton)


if __name__ == "__main__":
    config = AppConfig(
        database_url="mysql://localhost:3306/mydb",
        enable_feature_x=True,
        enable_feature_y=False,
    )

    injector = Injector(GreetingModule(config))

    app_config = injector.get(AppConfig)

    print(app_config)

    greeting_strategy = injector.get(GreetingType.HOLIDAY.value)

    print(greeting_strategy)
