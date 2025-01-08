from enum import Enum

from .greeting_strategies import (
    BasicGreetingStrategy,
    HolidayGreetingStrategy,
    TimeBasedGreetingStrategy,
)


class GreetingType(Enum):
    HOLIDAY = HolidayGreetingStrategy
    TIME_BASED = TimeBasedGreetingStrategy
    BASIC = BasicGreetingStrategy
