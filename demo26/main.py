import functools
import time


def time_logger(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        print(
            f"[TIME_LOGGER] Calling {func.__name__} with args={args}, kwargs={kwargs}"
        )
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(
            f"[TIME_LOGGER] {func.__name__} returned {result} (elapsed: {elapsed:.4f}s)"
        )
        return result

    return wrapper


def aspect_for_all_methods(method_decorator):

    def class_decorator(cls):
        # Go through the class’s dictionary items
        for name, attr in list(cls.__dict__.items()):
            # Only wrap callable attributes that are not dunder
            if callable(attr) and not name.startswith("__"):
                # Apply the decorator
                wrapped_method = method_decorator(attr)
                setattr(cls, name, wrapped_method)
        return cls

    return class_decorator


@aspect_for_all_methods(time_logger)
class Foo:
    """
    Every non-dunder method in Foo will be wrapped by time_logger.
    """

    def do_something(self, x, y):
        return x + y

    def long_operation(self):
        time.sleep(0.5)
        return "Finished long operation."


if __name__ == "__main__":
    f = Foo()
    print(f.do_something(3, 4))
    print(f.long_operation())
    print(f.long_operation())
