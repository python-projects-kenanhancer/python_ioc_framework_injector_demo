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


class GreetingModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(GreetingType.HOLIDAY.value, to=HolidayGreeting, scope=singleton)
        binder.bind(
            GreetingType.TIME_BASED.value, to=TimeBasedGreeting, scope=singleton
        )
        binder.bind(GreetingType.BASIC.value, to=BasicGreeting, scope=singleton)


def test_greeting_strategy(injector: Injector, greeting_type: GreetingType):

    greeting_strategy = injector.get(greeting_type.value)

    print(greeting_strategy)


if __name__ == "__main__":
    injector = Injector(GreetingModule)

    test_greeting_strategy(injector, GreetingType.HOLIDAY)

    test_greeting_strategy(injector, GreetingType.TIME_BASED)
