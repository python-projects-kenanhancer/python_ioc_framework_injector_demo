from typing import Any, Callable

from .context import Context


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
