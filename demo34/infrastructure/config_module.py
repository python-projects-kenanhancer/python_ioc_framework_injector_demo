from injector import Module, provider, singleton

from .models import (
    DatadogSettings,
    GreetingLanguage,
    GreetingType,
    SayHelloSettings,
    Settings,
)


class ConfigModule(Module):
    def __init__(self, gcs_bucket_name: str, gcs_blob_name: str):
        self.gcs_bucket_name = gcs_bucket_name
        self.gcs_blob_name = gcs_blob_name

    @provider
    @singleton
    def provide_settings(self) -> Settings:

        datadog = DatadogSettings(
            service="",
            environment="dev",
            project_id="",
            repo_name="",
            team="",
            log_level="INFO",
            logger_name="",
        )

        return Settings(datadog=datadog)

    @provider
    @singleton
    def provide_say_hello_settings(self) -> SayHelloSettings:

        return SayHelloSettings(
            default_name="World",
            greeting_type=GreetingType.TIME_BASED,
            greeting_language=GreetingLanguage.EN,
        )
