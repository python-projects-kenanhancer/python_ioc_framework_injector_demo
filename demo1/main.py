from injector import Injector

from configuration_module import ConfigurationModule
from database_service import DatabaseService
from demo1.greeting_service import GreetingService

if __name__ == '__main__':
    injector = Injector([ConfigurationModule()])
    database_service = injector.get(DatabaseService)
    database_service.connect()

    greeting_service = injector.get(GreetingService)
    print(greeting_service.greet("World"))
