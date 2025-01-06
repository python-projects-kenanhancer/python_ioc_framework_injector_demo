from injector import Injector, inject

from .models import AppConfig


class GreetingService:
    @inject
    def __init__(self, app_config: AppConfig, injector: Injector):
        self._app_config = app_config
        self._injector = injector

    def greet(self, name: str) -> str:
        strategy_enum = self._app_config.greeting_strategy
        greeting_strategy = self._injector.get(strategy_enum.value)
        return greeting_strategy.get_greeting_prefix(name)
