import time

from ..pipeline import Context, Next


def time_middleware(context: Context, next: Next):
    start = time.time()
    print("[TIME] Start timing...")
    result = next()
    elapsed = time.time() - start
    print(f"[TIME] {context.func.__name__} took {elapsed:.4f}s")
    return result
