from typing import Any, Callable


class Context:
    def __init__(self, func: Callable[..., Any], args: tuple, kwargs: dict):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.result = None
