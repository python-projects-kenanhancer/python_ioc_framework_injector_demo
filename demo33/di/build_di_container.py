from injector import Injector

from .config_module import ConfigModule
from .greeting_module import GreetingModule


def build_di_container():

    injector = Injector(
        [GreetingModule, ConfigModule("my-bucket", "configs/app-config.json")]
    )

    return injector
