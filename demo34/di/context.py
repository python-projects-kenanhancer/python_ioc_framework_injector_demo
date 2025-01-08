from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class Context:
    func: Callable[..., Any]
    args: tuple
    kwargs: dict
    result = None
