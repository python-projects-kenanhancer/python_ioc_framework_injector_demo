import inspect
from typing import Any, Callable, Type, Union

from .compose_middlewares import compose_middlewares
from .context import Context


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
