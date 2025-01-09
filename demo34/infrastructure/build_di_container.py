from injector import Injector

from .config_module import ConfigModule
from .greeting_module import GreetingModule
from .logging_module import LoggingModule


def build_di_container():

    injector = Injector(
        [
            LoggingModule,
            GreetingModule,
            ConfigModule("my-bucket", "configs/app-config.json"),
        ]
    )

    return injector
