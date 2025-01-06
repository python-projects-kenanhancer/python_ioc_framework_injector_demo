import functools
import time
from typing import Any, Callable


# 1. Define a Context dataclass (or simple class) to hold function info
class Context:
    """
    Holds information about the function call:
      - `func`: The original function to be called
      - `args`: Positional arguments
      - `kwargs`: Keyword arguments
      - `result`: (Optional) A place to store the final result
    """

    func: Callable[..., Any]
    args: tuple
    kwargs: dict
    result: Any

    def __init__(self, func: Callable[..., Any], args: tuple, kwargs: dict) -> None:
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.result = None


# 2. Our pipeline composer that returns a decorator-like function
def compose_middlewares(
    *middlewares: Callable[[Context, Callable[[], Any]], Any]
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Composes multiple middlewares into a single function decorator.

    Each middleware has the signature:
        def middleware(context: Context, next: Callable[[], Any]) -> Any

    The final function's signature is preserved via @functools.wraps.
    """

    def compose(final_func: Callable[..., Any]) -> Callable[..., Any]:
        # We'll preserve metadata about the original function
        @functools.wraps(final_func)
        def pipeline_call(*args: Any, **kwargs: Any) -> Any:
            ctx = Context(final_func, args, kwargs)

            def dispatch(index: int) -> Any:
                if index == len(middlewares):
                    # No more middlewares; call the actual function
                    ctx.result = ctx.func(*ctx.args, **ctx.kwargs)
                    return ctx.result

                # current middleware
                current_mw = middlewares[index]

                def next_call() -> Any:
                    return dispatch(index + 1)

                return current_mw(ctx, next_call)

            return dispatch(0)

        return pipeline_call

    return compose


# 3. A class decorator that applies the pipeline to all non-dunder methods
def pipeline(
    *middlewares: Callable[[Context, Callable[[], Any]], Any]
) -> Callable[[type], type]:
    """
    A class decorator that applies `compose_middlewares(middlewares...)`
    to every callable, non-dunder method in the class.
    """

    def class_decorator(cls: type) -> type:
        # Build a single "pipeline decorator" from these middlewares
        pipeline_decorator = compose_middlewares(*middlewares)

        for name, attr in list(cls.__dict__.items()):
            if callable(attr) and not name.startswith("__"):
                # Use pipeline_decorator on this method
                # pipeline_decorator returns a function that wraps 'attr'
                wrapped_method = pipeline_decorator(attr)
                setattr(cls, name, wrapped_method)

        return cls

    return class_decorator


# 4. Example middlewares:
def logger_middleware(context: Context, next_: Callable[[], Any]) -> Any:
    print(
        f"[LOGGER] About to call {context.func.__name__}"
        f" with args={context.args}, kwargs={context.kwargs}"
    )
    result = next_()
    print(f"[LOGGER] Finished calling {context.func.__name__}, result={result}")
    return result


def time_middleware(context: Context, next_: Callable[[], Any]) -> Any:
    start = time.time()
    print("[TIME] Start timing...")
    result = next_()
    elapsed = time.time() - start
    print(f"[TIME] {context.func.__name__} took {elapsed:.4f}s")
    return result


# 5. Usage
@pipeline(logger_middleware, time_middleware)
class Foo:
    """
    All non-dunder methods in Foo will be wrapped by the pipeline
    composed of `logger_middleware` and `time_middleware`.
    """

    def do_something(self, x: int, y: int) -> int:
        """Example method that just adds x + y."""
        print(f"Inside do_something: x={x}, y={y}")
        return x + y

    def long_operation(self) -> str:
        """Simulate a longer operation."""
        time.sleep(0.5)
        return "Finished long operation"


# 6. Demo
if __name__ == "__main__":
    f = Foo()
    result = f.do_something(3, 4)
    print("Final result from do_something:", result)

    result_long = f.long_operation()
    print("Final result from long_operation:", result_long)
    print("Final result from long_operation:", result_long)
