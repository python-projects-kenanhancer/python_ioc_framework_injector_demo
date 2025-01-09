from time import time

from injector import inject

from ..logger import LoggerStrategy
from ..pipeline import Context, Next


class TimeMiddleware:
    @inject
    def __init__(self, logger: LoggerStrategy):
        self.logger = logger

    def __call__(self, context: Context, next: Next):
        start = time()
        self.logger.info("[TIME] Start timing...")
        result = next()
        elapsed = time() - start
        self.logger.info(f"[TIME] {context.func.__name__} took {elapsed:.4f}s")
        return result
