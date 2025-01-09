import inspect

from flask import Request

from ..pipeline import Context, Next


def typed_request_middleware(context: Context, next: Next):
    """Middleware that handles both Flask Request and typed model input."""
    func = context.func
    args = context.args

    # 1. Get function signature info
    sig = inspect.signature(func)
    parameters = list(sig.parameters.values())
    if not parameters:
        raise TypeError(
            f"Function {func.__name__} has no parameters. Cannot infer typed request parameter."
        )

    # 2. Check first parameter type annotation
    first_param = parameters[0]
    annotated_type = first_param.annotation
    if annotated_type is inspect._empty:
        raise TypeError(
            f"Function {func.__name__}'s first parameter '{first_param.name}' "
            "is not annotated with a type. Please provide a type annotation."
        )

    # 3. Check first argument
    if not args:
        raise ValueError("No arguments provided at runtime.")

    maybe_request = args[0]

    # If the argument is already the correct type, pass it through
    if isinstance(maybe_request, annotated_type):
        return next()

    # If it's a Flask Request, process it
    if isinstance(maybe_request, Request):
        flask_request: Request = maybe_request
        # Process Flask request data
        json_data = flask_request.get_json(silent=True) or {}
        query_data = dict(flask_request.args)
        header_data = {}  # or parse headers if needed
        merged_data = {**json_data, **query_data, **header_data}

        # Convert to typed object
        if not hasattr(annotated_type, "from_dict"):
            raise AttributeError(
                f"Type '{annotated_type.__name__}' does not have a 'from_dict' method."
            )
        typed_obj = annotated_type.from_dict(merged_data)

        # Replace first argument
        context.args = (typed_obj,) + args[1:]

    else:
        raise TypeError(
            f"Expected first argument to be either {annotated_type.__name__} "
            f"or Flask Request, but got {type(maybe_request)}"
        )

    return next()
