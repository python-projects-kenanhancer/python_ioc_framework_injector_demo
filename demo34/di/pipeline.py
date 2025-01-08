import functools
import inspect
from dataclasses import dataclass
from typing import (
    Any,
    Callable,
    Protocol,
    TypeGuard,
    TypeVar,
    Union,
    cast,
    runtime_checkable,
)


@dataclass
class Context:
    func: Callable[..., Any]
    args: tuple
    kwargs: dict
    result = None


T = TypeVar("T")
R = TypeVar("R")


# Basic types
Next = Callable[[], Any]
TargetFunc = Callable[..., Any]


@runtime_checkable
class MiddlewareProtocol(Protocol):
    def __call__(self, context: Context, next: Next) -> Any: ...


@runtime_checkable
class PipelineFunction(Protocol):
    __is_pipeline__: bool

    def __call__(self, *args: Any, **kwargs: Any) -> Any: ...


# Middleware types
MiddlewareClass = type[MiddlewareProtocol]
MiddlewareFunc = Callable[[Context, Next], Any]
PipelineDecorator = Callable[[TargetFunc], PipelineFunction]

# Combined type for all valid pipeline items
PipelineItem = Union[
    MiddlewareClass,  # Class with __call__(self, context, next)
    MiddlewareFunc,  # Function taking (context, next)
    PipelineDecorator,  # Pipeline decorator
    # PipelineFunction,  # A function marked with __is_pipeline__
]


def clean_kwargs_for_target(
    func: TargetFunc, args: tuple, kwargs: dict[str, Any]
) -> dict[str, Any]:
    """
    Clean kwargs by removing values that are already provided in args
    to avoid "multiple values for argument" error
    """
    sig = inspect.signature(func)
    param_names = set(sig.parameters.keys())

    has_var_keyword = any(
        p.kind == inspect.Parameter.VAR_KEYWORD for p in sig.parameters.values()
    )

    # Get parameter names that are already filled by args
    bound_args = sig.bind_partial(*args)
    args_params = set(bound_args.arguments.keys())

    if not has_var_keyword:
        # Filter kwargs: must be in param_names AND not already in args
        return {
            k: v for k, v in kwargs.items() if k in param_names and k not in args_params
        }

    # If function has **kwargs, only filter out args params
    return {k: v for k, v in kwargs.items() if k not in args_params}


def is_middleware_func(item: Any) -> bool:
    return (
        callable(item)
        and not inspect.isclass(item)
        and len(inspect.signature(item).parameters) == 2  # context, next
    )


def is_middleware_class(item: Any) -> TypeGuard[MiddlewareProtocol]:
    """Check if item is a class implementing the MiddlewareProtocol."""
    return inspect.isclass(item) and issubclass(item, MiddlewareProtocol)


def is_pipeline_decorator(item: Any) -> TypeGuard[PipelineFunction]:
    return isinstance(item, PipelineFunction)


def create_middleware_from_pipeline(
    pipeline_decorator: PipelineDecorator,
) -> MiddlewareFunc:

    def middleware(context: Context, next: Next) -> Any:
        @pipeline_decorator
        @functools.wraps(context.func)
        def temp_func(*args: Any, **kwargs: Any) -> Any:
            return next()

        return temp_func(*context.args, **context.kwargs)

    return middleware


def create_middleware_from_class(cls: Any) -> MiddlewareFunc:

    def resolver(context: Context, next: Next) -> Any:
        injector = context.kwargs.get("injector")
        if not injector:
            raise RuntimeError(
                f"No injector found in context.kwargs while trying to resolve {cls}."
            )
        instance = injector.get(cls)
        return instance(context, next)

    return resolver


def create_middleware(item: Any) -> MiddlewareFunc:
    if is_middleware_class(item):
        return create_middleware_from_class(item)
    elif is_middleware_func(item):
        return item
    elif is_pipeline_decorator(item):
        return create_middleware_from_pipeline(item)
    else:
        raise ValueError(f"Invalid pipeline item: {item}")


def create_function_pipeline(
    middlewares: list[MiddlewareFunc],
) -> Callable[[TargetFunc], PipelineFunction]:
    """Create a pipeline for functions."""

    def function_decorator(target_func: TargetFunc) -> PipelineFunction:
        @functools.wraps(target_func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            ctx = Context(target_func, args, kwargs)

            def dispatch(index: int) -> Any:
                if index == len(middlewares):
                    clean_kwargs = clean_kwargs_for_target(
                        ctx.func, ctx.args, ctx.kwargs
                    )
                    return ctx.func(*ctx.args, **clean_kwargs)
                return middlewares[index](ctx, lambda: dispatch(index + 1))

            return dispatch(0)

        wrapper_with_mark = cast(PipelineFunction, wrapper)
        wrapper_with_mark.__is_pipeline__ = True
        return wrapper_with_mark

    return function_decorator


def create_class_pipeline(middlewares: list[MiddlewareFunc]) -> Callable[[type], type]:
    """Create a pipeline for classes."""

    def class_decorator(cls: type) -> type:
        method_names = [
            name
            for name, value in cls.__dict__.items()
            if callable(value) and not name.startswith("__")
        ]

        for name in method_names:
            original_method = getattr(cls, name)
            function_pipeline = create_function_pipeline(middlewares)
            decorated_method = function_pipeline(original_method)
            setattr(cls, name, decorated_method)

        return cls

    return class_decorator


def pipeline(*items: PipelineItem) -> PipelineFunction:

    filtered_items = [item for item in items if item not in (None, "")]
    middlewares: list[MiddlewareFunc] = []

    for item in filtered_items:
        try:
            middlewares.append(create_middleware(item))
        except ValueError as e:
            raise ValueError(f"Error creating middleware: {str(e)}")

    def decorator(target: Union[TargetFunc, type]) -> Union[PipelineFunction, type]:
        if isinstance(target, type):
            return create_class_pipeline(middlewares)(target)
        return create_function_pipeline(middlewares)(target)

    decorator_with_mark = cast(PipelineFunction, decorator)
    decorator_with_mark.__is_pipeline__ = True
    return decorator_with_mark


__all__ = [
    "pipeline",
    "Context",
    "Next",
    "MiddlewareClass",
    "MiddlewareFunc",
    "MiddlewareProtocol",
    "PipelineDecorator",
    "PipelineItem",
]
