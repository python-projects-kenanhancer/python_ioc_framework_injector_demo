import functools
import inspect
import time
from typing import Any, Callable


def build_param_strs(func: Callable, args: tuple, kwargs: dict) -> list[str]:
    """
    Given a function `func` and its call-time `args`, `kwargs`,
    returns a list of parameter strings in the form:
      [ "paramName:annotatedType=value", ... ]

    Special case:
      - If `paramName == "self"` and no annotation is provided,
        display `<class 'Foo'>` for clarity.
      - If no annotation is provided (and it's not `self`), use "?".
      - For `self`, we abbreviate the value with '...'.
    """
    sig = inspect.signature(func)
    bound_args = sig.bind(*args, **kwargs)
    bound_args.apply_defaults()

    param_strs = []

    for param_name, param_value in bound_args.arguments.items():
        param = sig.parameters[param_name]

        # Determine the annotated type (if any).
        if param.annotation is inspect.Parameter.empty:
            # If it's 'self' without annotation, show the class name for clarity.
            if param_name == "self":
                annotated_type = f"<class '{param_value.__class__.__name__}'>"
            else:
                annotated_type = "?"
        else:
            annotated_type = param.annotation

        # For `self`, we might display something like "self:<class 'Foo'>=..."
        # For others, we do "x:<class 'int'>=5"
        if param_name == "self":
            param_strs.append(f"{param_name}:{annotated_type}=...")
        else:
            param_strs.append(f"{param_name}:{annotated_type}={param_value}")

    return param_strs


def time_logger(func: Callable) -> Callable:
    """
    A decorator that logs:
      - Function name
      - Parameter names, annotated types, and values
      - Execution time
      - Return value
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        # Use our helper to build a list of nicely formatted parameter strings.
        param_strs = build_param_strs(func, args, kwargs)

        start = time.time()
        print(f"[TIME_LOGGER] Calling {func.__name__}({', '.join(param_strs)})")

        result = func(*args, **kwargs)

        elapsed = time.time() - start
        print(
            f"[TIME_LOGGER] {func.__name__} returned {result} (elapsed: {elapsed:.4f}s)"
        )
        return result

    return wrapper


def aspect_for_all_methods(method_decorator: Callable) -> Callable:
    """
    A class-decorator factory that applies `method_decorator` to
    all non-dunder methods in the class.
    """

    def class_decorator(cls):
        for name, attr in list(cls.__dict__.items()):
            if callable(attr) and not name.startswith("__"):
                wrapped_method = method_decorator(attr)
                setattr(cls, name, wrapped_method)
        return cls

    return class_decorator


@aspect_for_all_methods(time_logger)
class Foo:
    """All non-dunder methods in Foo will be wrapped by `time_logger`."""

    def do_something(self, x: int, y: int) -> int:
        """Add x and y."""
        return x + y

    def long_operation(self) -> str:
        """Simulate a longer task."""
        time.sleep(0.5)  # simulate some work
        return "Finished long operation."


if __name__ == "__main__":
    f = Foo()
    print(f.do_something(3, 4))
    print(f.long_operation())
    print(f.long_operation())
