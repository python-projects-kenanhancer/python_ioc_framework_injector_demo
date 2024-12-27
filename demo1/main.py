from configuration_module import ConfigurationModule
from database_service import DatabaseService
from greeting_service import GreetingService
from injector import Injector

if __name__ == "__main__":
    injector = Injector([ConfigurationModule()])
    database_service = injector.get(DatabaseService)
    database_service.connect()

    greeting_service = injector.get(GreetingService)
    print(greeting_service.greet("World"))
