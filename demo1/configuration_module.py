from injector import Module, provider, Injector, singleton
from app_config import AppConfig


class ConfigurationModule(Module):
    @provider
    @singleton
    def provide_app_config(self) -> AppConfig:
        database_url = "sqlite:///db.sqlite"
        return AppConfig(database_url=database_url)
