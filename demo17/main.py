import logging
import os
from functools import wraps
from inspect import Parameter, signature

# Configure logging
# Setup logger for the library
logger = logging.getLogger("KENAN_IOC")
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logger.setLevel(log_level)  # Set the desired log level

# Temporary handler setup for development or testing
stream_handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


def class_inject(cls):
    # Get the signature of the class constructor (__init__)
    if cls.__init__ is not object.__init__:  # Ensure there is a custom constructor
        sig = signature(cls.__init__)
        constructor_params = ", ".join(
            f"{name}: {param.annotation.__name__ if param.annotation != param.empty else 'Any'}"
            for name, param in sig.parameters.items()
            if name != "self"
        )
        logger.info(f"Class {cls.__name__} constructor signature: {constructor_params}")
    else:
        logger.info(f"Class {cls.__name__} uses default constructor.")

    return cls


def constructor_inject(constructor):
    original_sig = signature(constructor)

    @wraps(constructor)
    def wrapped_constructor(*args, **kwargs):
        # Resolve class name from the constructor or its class
        cls_name = constructor.__qualname__.split(".<locals>", 1)[0].rsplit(".", 1)[0]

        # Prepare parameter details for logger
        constructor_params = ", ".join(
            f"{name}: {param.annotation.__name__ if param.annotation != Parameter.empty else 'Any'}"
            for name, param in original_sig.parameters.items()
            if name != "self"  # Exclude 'self' from constructor parameters
        )

        # Log the constructor call details (assuming lifecycle context is handled elsewhere or not needed here)
        logger.debug(
            f"Resolving class {cls_name} with constructor params: {constructor_params}"
        )

        # Call the original constructor
        return constructor(*args, **kwargs)

    return wrapped_constructor


# Application classes
class AppConfig:
    def __init__(self, database_url="https://db.example.com"):
        self.database_url = database_url


@class_inject
class DatabaseService:
    @constructor_inject
    def __init__(self, app_config: AppConfig):
        self.app_config = app_config

    def connect(self):
        logger.info(f"Connecting to database at {self.app_config.database_url}")


if __name__ == "__main__":
    app_config = AppConfig()
    database_service = DatabaseService(app_config)
    database_service.connect()
