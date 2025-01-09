from ..build_di_container import build_di_container
from ..pipeline import Context, Next


def container_builder_middleware(context: Context, next: Next):
    if "injector" not in context.kwargs:
        container = build_di_container()
        context.kwargs["injector"] = container
    return next()
