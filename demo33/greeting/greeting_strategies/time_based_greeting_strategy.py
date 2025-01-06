from .greeting_strategy import GreetingStrategy


class TimeBasedGreetingStrategy(GreetingStrategy):
    def get_greeting_prefix(self, name: str) -> str:
        return f"Good day, {name}!"
