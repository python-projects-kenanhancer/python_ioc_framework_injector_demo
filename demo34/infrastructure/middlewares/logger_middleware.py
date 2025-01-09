from ..pipeline import Context, Next


def logger_middleware(context: Context, next: Next):
    print(
        f"[LOGGER] About to call {context.func.__name__}"
        f" with args={context.args}, kwargs={context.kwargs}"
    )
    result = next()
    print(f"[LOGGER] Finished {context.func.__name__}, result={result}")
    return result
