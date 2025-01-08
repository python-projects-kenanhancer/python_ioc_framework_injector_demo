from .greeting_strategy import GreetingStrategy


class HolidayGreetingStrategy(GreetingStrategy):
    def get_greeting_prefix(self, name: str) -> str:
        return f"Happy Holidays, {name}!"
