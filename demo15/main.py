class IoCContainer:
    def __init__(self):
        self.providers = {}
        self.instances = {}
        self.pre_hooks = []
        self.post_hooks = []

    def add_pre_hook(self, hook):
        self.pre_hooks.append(hook)

    def add_post_hook(self, hook):
        self.post_hooks.append(hook)

    def resolve(self, cls):
        if cls in self.instances:
            return self.instances[cls]

        for hook in self.pre_hooks:
            hook(cls)

        if cls not in self.providers:
            self.providers[cls] = lambda: cls()

        instance = self.providers[cls]()

        for hook in self.post_hooks:
            hook(instance)

        self.instances[cls] = instance
        return instance


def inject(constructor):
    from inspect import signature, Parameter
    sig = signature(constructor)

    def wrapper(*args, **kwargs):
        bound = sig.bind_partial(*args, **kwargs)
        bound.apply_defaults()

        new_args = list(bound.args)
        for name, param in sig.parameters.items():
            if param.annotation is not Parameter.empty and isinstance(param.annotation, type):
                if name in bound.arguments:
                    # Resolve only if the type is a class and needs to be instantiated
                    bound.arguments[name] = container.resolve(param.annotation)
                elif param.default is Parameter.empty:
                    # If there is no default and no argument provided, resolve it
                    bound.arguments[name] = container.resolve(param.annotation)

        return constructor(*bound.args, **bound.kwargs)

    return wrapper


# Application classes
class AppConfig:
    def __init__(self, database_url="https://db.example.com"):
        self.database_url = database_url


class DatabaseService:
    @inject
    def __init__(self, app_config: AppConfig):
        self.app_config = app_config

    def connect(self):
        print(f"Connecting to database at {self.app_config.database_url}")


# Hooks
def pre_instantiation_hook(cls):
    print(f"Creating instance of {cls.__name__}...")


def post_instantiation_hook(instance):
    print(f"Instance of {instance.__class__.__name__} created with id {id(instance)}")


if __name__ == '__main__':
    container = IoCContainer()

    # Set up hooks
    container.add_pre_hook(pre_instantiation_hook)
    container.add_post_hook(post_instantiation_hook)

    # Using the IoC container
    db_service = container.resolve(DatabaseService)
    db_service.connect()
