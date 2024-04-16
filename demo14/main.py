import functools
import logging
import time

logging.getLogger().setLevel(logging.INFO)


def log_method_calls(func):
    """Method decorator for logging method calls."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f"BEGIN Method: {func.__name__} Args:{args} Kwargs:{kwargs}")
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        duration = end_time - start_time
        logging.info(f"END Method: {func.__name__} Result:{result} Duration:{duration:.3f}")
        return result

    return wrapper


def handle_errors(func):
    """Method decorator for error handling."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"ERROR Method: {func.__name__} Error: {str(e)}")
            raise e  # Optionally, you could handle the error or suppress it

    return wrapper


def logger(cls):
    """Class decorator that applies logging to all methods."""
    for name, method in cls.__dict__.items():
        if callable(method) and not name.startswith('__'):
            setattr(cls, name, log_method_calls(method))
    return cls


def error(cls):
    """Class decorator that applies error handling to all methods."""
    for name, method in cls.__dict__.items():
        if callable(method) and not name.startswith('__'):
            setattr(cls, name, handle_errors(method))
    return cls


@error
@logger
class GreetingHelper:
    def get_full_name(self, first_name: str, last_name: str):
        return f"{first_name} {last_name}"


@error
@logger
class EnglishGreeting:
    def __init__(self, greeting_helper: GreetingHelper):
        self.greeting_helper = greeting_helper

    def say_hello(self, first_name, last_name):
        return f"Hello, {self.greeting_helper.get_full_name(first_name, last_name)}!"

    def say_goodbye(self, first_name, last_name):
        return f"Goodbye, {self.greeting_helper.get_full_name(first_name, last_name)}!"


if __name__ == '__main__':
    greeting_helper = GreetingHelper()
    greeter = EnglishGreeting(greeting_helper)
    logging.info(greeter.say_hello("John", "John"))
    logging.info(greeter.say_goodbye("Andy", "Andy"))
