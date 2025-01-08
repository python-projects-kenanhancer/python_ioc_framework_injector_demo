from .greeting_strategy import GreetingStrategy


class BasicGreetingStrategy(GreetingStrategy):
    def get_greeting_prefix(self, name: str) -> str:
        return f"Hello, {name}!"
