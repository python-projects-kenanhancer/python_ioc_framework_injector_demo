from typing import cast

from infrastructure import SayHelloSettings
from injector import Injector, inject

from .greeting_strategies import GreetingStrategy


class GreetingService:
    @inject
    def __init__(self, say_hello_settings: SayHelloSettings, injector: Injector):
        self._say_hello_settings = say_hello_settings
        self._injector = injector

    def greet(self, name: str) -> str:
        strategy_enum = self._say_hello_settings.greeting_type
        greeting_strategy = cast(
            GreetingStrategy, self._injector.get(strategy_enum.value)
        )
        return greeting_strategy.get_greeting_prefix(name)
