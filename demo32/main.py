import inspect
from time import time
from typing import Any, Callable, Type, Union

from pydantic import BaseModel, ConfigDict


class Context:
    def __init__(self, func: Callable[..., Any], args: tuple, kwargs: dict):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.result = None


def compose_middlewares(
    *middlewares: Callable[[Context, Callable[[], Any]], Any]
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Returns a decorator that applies all the given middlewares in order
    to a single function.
    """

    def decorator(final_func: Callable[..., Any]) -> Callable[..., Any]:
        # We'll preserve metadata about the original function using `functools.wraps`
        import functools

        @functools.wraps(final_func)
        def pipeline_call(*args: Any, **kwargs: Any) -> Any:
            ctx = Context(final_func, args, kwargs)

            def dispatch(index: int) -> Any:
                if index == len(middlewares):
                    # No more middlewares, call the original function
                    ctx.result = ctx.func(*ctx.args, **ctx.kwargs)
                    return ctx.result
                current_mw = middlewares[index]

                def next_() -> Any:
                    return dispatch(index + 1)

                return current_mw(ctx, next_)

            return dispatch(0)

        return pipeline_call

    return decorator


def pipeline(
    *middlewares: Callable[[Context, Callable[[], Any]], Any]
) -> Callable[[Union[Type, Callable[..., Any]]], Union[Type, Callable[..., Any]]]:
    """
    A decorator factory that, depending on what it’s decorating, either:
      - wraps a *single function/method*, OR
      - wraps *all public methods* in a class,
    using the given middlewares.
    """

    # Reuse our single-function composer
    single_decorator = compose_middlewares(*middlewares)

    def decorator(
        target: Union[Type, Callable[..., Any]]
    ) -> Union[Type, Callable[..., Any]]:
        if inspect.isclass(target):
            # --- Case 1: `target` is a class ---
            cls = target
            for name, attr in list(cls.__dict__.items()):
                if callable(attr) and not name.startswith("__"):
                    # Replace method with pipeline
                    wrapped_method = single_decorator(attr)
                    setattr(cls, name, wrapped_method)
            return cls
        else:
            # --- Case 2: `target` is a function/method ---
            func = target
            return single_decorator(func)

    return decorator


def logger_middleware(context: Context, next_: Callable[[], Any]) -> Any:
    print(
        f"[LOGGER] About to call {context.func.__name__}"
        f" with args={context.args}, kwargs={context.kwargs}"
    )
    result = next_()
    print(f"[LOGGER] Finished {context.func.__name__}, result={result}")
    return result


def time_middleware(context: Context, next_: Callable[[], Any]) -> Any:
    start = time()
    print("[TIME] Start timing...")
    result = next_()
    elapsed = time() - start
    print(f"[TIME] {context.func.__name__} took {elapsed:.4f}s")
    return result


@pipeline(logger_middleware, time_middleware)
class Foo:
    def do_something(self, x: int, y: int) -> int:
        print(f"Inside do_something: x={x}, y={y}")
        return x + y

    def long_operation(self) -> str:
        import time

        time.sleep(0.5)
        return "Finished operation"


@pipeline(logger_middleware, time_middleware)  # only logs, for example
def add_numbers(a: int, b: int) -> int:
    print(f"Inside add_numbers: a={a}, b={b}")
    return a + b


class GreetingHttpRequest(BaseModel):
    first_name: str
    last_name: str

    model_config = ConfigDict(from_attributes=True)

    def to_dict(self) -> dict:
        # The typed decorator will call this to serialize the response
        return self.model_dump()

    @classmethod
    def from_dict(cls, data: dict):
        # The typed decorator will call this to parse incoming JSON
        return cls.model_validate(data)


@pipeline(logger_middleware, time_middleware)  # only logs, for example
def say_hello_ultimate_http(request: GreetingHttpRequest):
    full_name = f"{request.first_name} {request.last_name}"

    return f"Hello, {full_name}"


if __name__ == "__main__":

    request_obj = GreetingHttpRequest(first_name="John", last_name="Doe")

    say_hello_ultimate_http(request_obj)

    print(add_numbers(3, 4))

    f = Foo()
    result = f.do_something(2, 5)
    print("Got result:", result)
    print(f.long_operation())
    print(f.long_operation())
