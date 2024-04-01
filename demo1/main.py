from injector import Injector

from configuration_module import ConfigurationModule
from database_service import DatabaseService

if __name__ == '__main__':
    injector = Injector([ConfigurationModule()])
    database_service = injector.get(DatabaseService)
    database_service.connect()