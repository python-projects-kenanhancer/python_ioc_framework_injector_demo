import functools
import inspect
import time
from functools import reduce
from typing import Callable


def compose_decorators(*decorators: Callable) -> Callable:
    """
    Returns a single decorator that applies all `decorators` in sequence.
    Example: compose_decorators(A, B)(func) -> A(B(func))
    """

    def combined_decorator(func: Callable) -> Callable:
        for deco in reversed(decorators):
            func = deco(func)  # apply each decorator in the order provided
        return func

    return combined_decorator


def compose_decorators_v2(*decorators: Callable) -> Callable:
    """
    Returns a single decorator that applies all `decorators` in order,
    so compose_decorators(A, B)(func) -> A(B(func)).

    The first decorator in the list becomes the outermost at runtime.
    """

    def combined_decorator(func: Callable) -> Callable:
        # We iterate in reverse so that the *first* decorator
        # is applied last, making it the outermost wrapper at runtime.
        # reduce() takes an initial value (func) and applies each decorator in turn.
        return reduce(lambda acc, deco: deco(acc), reversed(decorators), func)

    return combined_decorator


def aspect_for_all_methods(*method_decorators: Callable) -> Callable:
    """
    A class decorator that applies *all* `method_decorators` to every
    callable, non-dunder method in the class.
    """

    def class_decorator(cls):
        # Compose all decorators into a single decorator
        combined = compose_decorators_v2(*method_decorators)

        for name, attr in list(cls.__dict__.items()):
            # only wrap callable, non-dunder attributes
            if callable(attr) and not name.startswith("__"):
                setattr(cls, name, combined(attr))

        return cls

    return class_decorator


def log_calls(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Build a param string
        sig = inspect.signature(func)
        bound = sig.bind(*args, **kwargs)
        bound.apply_defaults()
        params_str = ", ".join(
            f"{name}={value!r}" for name, value in bound.arguments.items()
        )
        print(f"[LOG] Calling {func.__name__}({params_str})")
        result = func(*args, **kwargs)
        print(f"[LOG] {func.__name__} returned {result!r}")
        return result

    return wrapper


def measure_time(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] measure time is started")
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"[TIME] {func.__name__} took {elapsed:.4f} seconds.")
        return result

    return wrapper


@aspect_for_all_methods(log_calls, measure_time)
class Foo:
    def do_something(self, x: int, y: int) -> int:
        """Add x and y."""
        return x + y

    def long_operation(self):
        """Simulate a work-intensive method."""
        time.sleep(0.5)
        return "Finished operation"


if __name__ == "__main__":
    f = Foo()
    print(f.do_something(3, 4))
    print(f.long_operation())
