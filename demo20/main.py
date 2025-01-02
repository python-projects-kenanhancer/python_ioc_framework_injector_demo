from enum import Enum

from injector import Binder, Injector, singleton


class HolidayGreeting:
    pass


class TimeBasedGreeting:
    pass


class BasicGreeting:
    pass


class GreetingType(Enum):
    HOLIDAY = HolidayGreeting
    TIME_BASED = TimeBasedGreeting
    BASIC = BasicGreeting


def configure_greeting_module(binder: Binder):
    binder.bind(GreetingType.HOLIDAY.value, to=HolidayGreeting, scope=singleton)
    binder.bind(GreetingType.TIME_BASED.value, to=TimeBasedGreeting, scope=singleton)
    binder.bind(GreetingType.BASIC.value, to=BasicGreeting, scope=singleton)


def test_greeting_strategy(injector: Injector, greeting_type: GreetingType):

    greeting_strategy = injector.get(greeting_type.value)

    print(greeting_strategy)


if __name__ == "__main__":
    injector = Injector(configure_greeting_module)

    test_greeting_strategy(injector, GreetingType.HOLIDAY)

    test_greeting_strategy(injector, GreetingType.TIME_BASED)
