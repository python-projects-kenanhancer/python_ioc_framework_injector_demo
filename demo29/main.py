import time
from typing import Any, Callable


def compose_middlewares(*middlewares: Callable) -> Callable:
    """
    Builds a pipeline of middlewares so that each middleware sees:
      (next_func, original_func, *args, **kwargs)
    and can decide if or how to call next_func(...).
    """

    def compose(final_func: Callable) -> Callable:
        """
        Given the final_func (e.g., Foo.do_something),
        returns a new function that runs the entire middleware chain.
        """

        def call_pipeline(*args, **kwargs) -> Any:
            """
            Entry point: call the first middleware (index=0).
            """

            return _dispatch(0, final_func, *args, **kwargs)

        def _dispatch(index: int, func: Callable, *args, **kwargs) -> Any:
            """
            Calls the middleware at `middlewares[index]`, passing it
            a next_func that calls _dispatch(index+1, ...).
            If we run out of middlewares, call `func(*args, **kwargs)`.
            """
            if index == len(middlewares):
                # No more middlewares; call the final function.
                return func(*args, **kwargs)

            current_middleware = middlewares[index]

            def next_func(next_func_target: Callable, *a, **kw) -> Any:
                """
                This is what the current middleware calls
                to invoke the next piece of the pipeline.
                Typically, 'next_func_target' == `func`
                or the same 'func' passed along, but in principle
                you could swap in a different target function if needed.
                """
                return _dispatch(index + 1, next_func_target, *a, **kw)

            # Call the current middleware with:
            # (next_func, func, *args, **kwargs)
            return current_middleware(next_func, func, *args, **kwargs)

        return call_pipeline

    return compose


def aspect_for_all_methods(*middlewares: Callable) -> Callable:
    """
    A class decorator that applies the given middlewares (Express-like)
    to all non-dunder methods in the class.
    """

    def class_decorator(cls):
        pipeline_decorator = compose_middlewares(*middlewares)

        for name, attr in list(cls.__dict__.items()):
            if callable(attr) and not name.startswith("__"):
                # Build the pipeline for this method
                wrapped_method = pipeline_decorator(attr)
                setattr(cls, name, wrapped_method)
        return cls

    return class_decorator


def logger_middleware(next_func, func, *args, **kwargs):
    print(f"[LOGGER] About to call {func.__name__} with args={args}, kwargs={kwargs}")
    result = next_func(func, *args, **kwargs)
    print(f"[LOGGER] Done calling {func.__name__}, result={result}")
    return result


def time_middleware(next_func, func, *args, **kwargs):

    start = time.time()
    print("[TIME] Timing start")
    result = next_func(func, *args, **kwargs)
    elapsed = time.time() - start
    print(f"[TIME] {func.__name__} took {elapsed:.4f}s")
    return result


@aspect_for_all_methods(logger_middleware, time_middleware)
class Foo:
    def do_something(self, x, y):
        print(f"Inside do_something: x={x}, y={y}")
        return x + y

    def long_operation(self):
        time.sleep(0.5)
        return "Finished operation"


if __name__ == "__main__":
    f = Foo()
    result = f.do_something(3, 4)
    print("Final result:", result)
    print(f.long_operation())
    print(f.long_operation())
