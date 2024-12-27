import logging
from functools import partial, wraps
from inspect import Parameter, signature

# Configure logging
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Create a logger for your library module
logger = logging.getLogger(__name__)
logger.addHandler(
    logging.NullHandler()
)  # Add NullHandler to prevent logging if no configuration is found


class IoCContainer:
    def __init__(self):
        self.providers = {}
        self.instances = {}
        self.middlewares = []

    def add_middleware(self, middleware):
        self.middlewares.append(middleware)

    def resolve(self, cls):
        lifecycle = getattr(cls, "_lifecycle", "transient")  # default to transient
        sig = signature(cls)
        constructor_params = ", ".join(
            f"{name}: {param.annotation.__name__ if param.annotation != Parameter.empty else 'Any'}"
            for name, param in sig.parameters.items()
            if name != "self"  # Exclude 'self' from constructor parameters
        )

        logging.debug(
            f"Resolving class {cls.__name__} with lifecycle: {lifecycle}. Constructor params: {constructor_params}"
        )

        # Check if a singleton instance already exists
        if lifecycle == "singleton" and cls in self.instances:
            logging.debug(f"Using existing singleton instance of {cls.__name__}")
            return self.instances[cls]

        # Create the middleware chain and instantiation
        def instantiate(cls, container):
            if cls not in container.providers:
                container.providers[cls] = lambda: cls()
            # logging.debug(f"Creating new instance of {cls.__name__}")
            return container.providers[cls]()

        result = instantiate
        for middleware in reversed(self.middlewares):
            result = partial(middleware, next=partial(result, cls, self))

        instance = result(cls, self)

        # Store the instance if it's a singleton
        if lifecycle == "singleton":
            self.instances[cls] = instance
            logging.debug(f"Stored {cls.__name__} as a singleton instance")

        return instance


def inject(constructor):
    sig = signature(constructor)

    @wraps(constructor)
    def wrapped_constructor(*args, **kwargs):
        bound = sig.bind_partial(*args, **kwargs)
        bound.apply_defaults()

        new_args = []
        for name, param in sig.parameters.items():
            if param.annotation is not param.empty:
                resolved = container.resolve(param.annotation)
                new_args.append(resolved)
            else:
                new_args.append(bound.arguments.get(name))

        return constructor(*new_args, **kwargs)

    return wrapped_constructor


def singleton(cls):
    original_sig = signature(cls)
    setattr(cls, "_lifecycle", "singleton")
    return cls


def transient(cls):
    setattr(cls, "_lifecycle", "transient")
    return cls


# Application classes
@singleton
class AppConfig:
    @inject
    def __init__(self, database_url="https://db.example.com"):
        self.database_url = database_url


@singleton
class DatabaseService:
    # @inject
    def __init__(self, app_config: AppConfig):
        self.app_config = app_config

    def connect(self):
        logging.info(f"Connecting to database at {self.app_config.database_url}")


# Middleware functions
def logging_middleware(cls, container, next):
    # logging.debug(f"Creating instance of {cls.__name__}...")
    instance = next()  # next is already bound to cls and container
    # logging.debug(f"Instance of {cls.__name__} created with id {id(instance)}")
    return instance


def singleton_check_middleware(cls, container, next):
    if cls in container.instances:
        logging.debug(f"Singleton check: Returning existing instance of {cls.__name__}")
        return container.instances[cls]
    return next()  # next is already bound to cls and container


if __name__ == "__main__":
    container = IoCContainer()
    container.add_middleware(logging_middleware)
    # container.add_middleware(singleton_check_middleware)

    # Using the IoC container
    db_service = container.resolve(DatabaseService)
    db_service2 = container.resolve(DatabaseService)
    db_service.connect()
    db_service2.connect()
