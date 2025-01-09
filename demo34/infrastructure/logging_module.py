from injector import Module, provider, singleton

from .logger import DatadogLoggerStrategy, LoggerStrategy
from .models import Settings


class LoggingModule(Module):
    @singleton
    @provider
    def provide_logger_strategy(self, settings: Settings) -> LoggerStrategy:

        datadog = settings.datadog

        if datadog is None:
            raise RuntimeError(
                "Datadog settings are required but not configured. "
                "Please check your Settings configuration."
            )

        return DatadogLoggerStrategy(
            service=datadog.service,
            project_id=datadog.project_id,
            environment=datadog.environment,
            repo_name=datadog.repo_name,
            team=datadog.team,
            log_level=datadog.log_level,
            logger_name=datadog.logger_name,
        )
