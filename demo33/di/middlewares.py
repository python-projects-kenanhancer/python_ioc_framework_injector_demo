import inspect
from time import time
from typing import Any, Callable

from flask import Request

from .build_di_container import build_di_container
from .context import Context


def logger_middleware(context: Context, next_: Callable[[], Any]) -> Any:
    print(
        f"[LOGGER] About to call {context.func.__name__}"
        f" with args={context.args}, kwargs={context.kwargs}"
    )
    result = next_()
    print(f"[LOGGER] Finished {context.func.__name__}, result={result}")
    return result


def time_middleware(context: Context, next_: Callable[[], Any]):
    start = time()
    print("[TIME] Start timing...")
    result = next_()
    elapsed = time() - start
    print(f"[TIME] {context.func.__name__} took {elapsed:.4f}s")
    return result


def typed_request_middleware(context: Context, next_: Callable[[], Any]):
    """Middleware that replaces the first argument (Flask Request)
    with a typed model derived from the request content."""

    func = context.func
    args = context.args

    # 1. Reflect on the original function's signature
    sig = inspect.signature(func)
    parameters = list(sig.parameters.values())
    if not parameters:
        raise TypeError(
            f"Function {func.__name__} has no parameters. "
            "Cannot infer typed request parameter."
        )

    # 2. The first parameter must have a type annotation, e.g. GreetingRequest
    first_param = parameters[0]
    annotated_type = first_param.annotation

    if annotated_type is inspect._empty:
        raise TypeError(
            f"Function {func.__name__}'s first parameter '{first_param.name}' "
            "is not annotated with a type. Please provide a type annotation."
        )

    # 3. We expect the first *runtime* argument to be a Flask Request
    if not args:
        raise ValueError("No arguments provided at runtime (expected a Flask Request).")

    maybe_request = args[0]
    if not isinstance(maybe_request, Request):
        raise TypeError(
            f"Expected the first argument to be a Flask Request, but got {type(maybe_request)}"
        )

    flask_request: Request = maybe_request

    # 4. Deserialize JSON body from the Flask Request
    json_data = flask_request.get_json(silent=True) or {}

    # 4.1. Query params as a dict
    query_data = dict(flask_request.args)

    # 4.2. (Optional) Headers or other data
    header_data = {}  # or parse headers if needed

    # Merge them in the order you want
    merged_data = {**json_data, **query_data, **header_data}

    # 5. Check if annotated_type has a `.from_dict(...)` method
    if not hasattr(annotated_type, "from_dict"):
        raise AttributeError(
            f"Type '{annotated_type.__name__}' does not have a 'from_dict' method."
        )

    # 6. Convert the JSON to a strongly typed model
    typed_obj = annotated_type.from_dict(merged_data)

    # 7. Replace the first argument with the typed object
    new_args = (typed_obj,) + args[1:]
    context.args = new_args

    # 8. Call the next middleware or final function
    result = next_()

    # 9. If the result has a `.to_dict()`, convert to dict so Flask can return JSON
    #    (Only if you want that automatically.)
    if hasattr(result, "to_dict") and callable(result.to_dict):
        return result.to_dict()

    return result


def inject_dependency_middleware(context: Context, next_: Callable[[], Any]) -> Any:
    """
    Middleware that uses a DI container (from context.kwargs["injector"])
    to inject parameters for the target function.

    - If the target function does NOT declare 'injector' as a parameter,
      we remove 'injector' from kwargs so Python won't complain about
      "unexpected keyword argument 'injector'".
    - We then do typed injection for any missing parameters that have type hints.
    """

    func = context.func
    original_args = context.args
    original_kwargs = dict(context.kwargs)  # make a copy so we can modify safely

    sig = inspect.signature(func)
    param_names = set(sig.parameters.keys())

    # Grab the injector object if any (from container_builder_middleware)
    injector_obj = original_kwargs.get("injector", None)

    # If the function does NOT declare 'injector', remove it from final kwargs
    # so that bind_partial won't complain about an extra param.
    if "injector" not in param_names and "injector" in original_kwargs:
        del original_kwargs["injector"]

    # Now bind partial with the safe set of kwargs
    bound_args = sig.bind_partial(*original_args, **original_kwargs)
    bound_args.apply_defaults()

    # For each unfilled parameter with a type annotation, attempt injection
    for param_name, param in sig.parameters.items():
        if param_name not in bound_args.arguments:
            annotated_type = param.annotation

            # If the param is typed, we try to get it from 'injector_obj'
            if annotated_type != inspect.Parameter.empty:
                if injector_obj is None:
                    # No injector found - user can decide to raise or skip
                    raise RuntimeError(
                        f"Cannot inject '{param_name}' (type={annotated_type}) "
                        f"because no injector is available. "
                        "Did you forget to add container_builder_middleware?"
                    )
                # Attempt to resolve from the injector
                dependency = injector_obj.get(annotated_type)
                bound_args.arguments[param_name] = dependency

    # Update context with the newly bound arguments
    context.args = bound_args.args
    context.kwargs = bound_args.kwargs

    return next_()


def container_builder_middleware(context: Context, next_: Callable[[], Any]) -> Any:
    container = build_di_container()
    context.kwargs["injector"] = container
    return next_()


__all__ = [
    "logger_middleware",
    "time_middleware",
    "typed_request_middleware",
    "inject_dependency_middleware",
    "container_builder_middleware",
]
