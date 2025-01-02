from abc import ABC, abstractmethod
from enum import Enum

from injector import Binder, Injector, Module, inject, provider, singleton


class GreetingStrategy(ABC):
    @abstractmethod
    def get_greeting_prefix(self, name: str) -> str:
        raise NotImplementedError


class BasicGreetingStrategy(GreetingStrategy):
    def get_greeting_prefix(self, name: str) -> str:
        return f"Hello, {name}!"


class HolidayGreetingStrategy(GreetingStrategy):
    def get_greeting_prefix(self, name: str) -> str:
        return f"Happy Holidays, {name}!"


class TimeBasedGreetingStrategy(GreetingStrategy):
    def get_greeting_prefix(self, name: str) -> str:
        return f"Good day, {name}!"


class GreetingType(Enum):
    HOLIDAY = HolidayGreetingStrategy
    TIME_BASED = TimeBasedGreetingStrategy
    BASIC = BasicGreetingStrategy


class AppConfig:
    def __init__(
        self,
        database_url: str,
        enable_feature_x: bool,
        enable_feature_y: bool,
        greeting_strategy: GreetingType,
    ):
        self.database_url = database_url
        self.enable_feature_x = enable_feature_x
        self.enable_feature_y = enable_feature_y
        self.greeting_strategy = greeting_strategy


class GreetingService:
    @inject
    def __init__(self, app_config: AppConfig, injector: Injector):
        self._app_config = app_config
        self._injector = injector

    def greet(self, name: str) -> str:
        strategy_enum = self._app_config.greeting_strategy
        greeting_strategy = self._injector.get(strategy_enum.value)
        return greeting_strategy.get_greeting_prefix(name)


class ConfigModule(Module):
    def __init__(self, gcs_bucket_name: str, gcs_blob_name: str):
        self.gcs_bucket_name = gcs_bucket_name
        self.gcs_blob_name = gcs_blob_name

    @provider
    @singleton
    def provide_app_config(self) -> AppConfig:
        # 1. Load/parse config from GCS:
        raw_dict = self._download_and_parse_config_from_gcs(
            self.gcs_bucket_name, self.gcs_blob_name
        )
        # 2. Convert raw_dict to AppConfig
        return AppConfig(
            database_url=raw_dict["database_url"],
            enable_feature_x=raw_dict["enable_feature_x"],
            enable_feature_y=raw_dict["enable_feature_y"],
            greeting_strategy=GreetingType[raw_dict["greeting_strategy"]],
        )

    def _download_and_parse_config_from_gcs(
        self, bucket_name: str, blob_name: str
    ) -> dict:
        # client = storage.Client()
        # bucket = client.bucket(bucket_name)
        # blob = bucket.blob(blob_name)
        # data = blob.download_as_text()      # returns your JSON as text
        # return json.loads(data)             # parse into dict

        return {
            "database_url": "mysql://localhost:3306/mydb",
            "enable_feature_x": True,
            "enable_feature_y": False,
            "greeting_strategy": "HOLIDAY",
        }


class GreetingModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(
            GreetingType.HOLIDAY.value, to=HolidayGreetingStrategy, scope=singleton
        )
        binder.bind(
            GreetingType.TIME_BASED.value, to=TimeBasedGreetingStrategy, scope=singleton
        )
        binder.bind(GreetingType.BASIC.value, to=BasicGreetingStrategy, scope=singleton)


if __name__ == "__main__":
    config = AppConfig(
        database_url="mysql://localhost:3306/mydb",
        enable_feature_x=True,
        enable_feature_y=False,
        greeting_strategy=GreetingType.HOLIDAY,
    )

    injector = Injector(
        [GreetingModule, ConfigModule("my-bucket", "configs/app-config.json")]
    )

    app_config = injector.get(AppConfig)

    print(app_config)

    greeting_strategy = injector.get(GreetingType.HOLIDAY.value)

    print(greeting_strategy)

    greeting_service = injector.get(GreetingService)

    print(greeting_service.greet("Kenan"))
