from app_config import AppConfig
from injector import Module, provider, singleton


class ConfigurationModule(Module):
    @provider
    @singleton
    def provide_app_config(self) -> AppConfig:
        database_url = "sqlite:///db.sqlite"
        return AppConfig(database_url=database_url)
