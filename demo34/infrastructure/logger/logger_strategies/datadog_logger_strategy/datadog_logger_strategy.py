import logging
from typing import Optional

from ..logger_strategy import LoggerStrategy
from .json_datadog_formatter import JsonDatadogFormatter


class DatadogLoggerStrategy(LoggerStrategy):
    """
    In high-volume scenarios, instead of sending each log message directly to Datadog via HTTP POST,
    it's generally more efficient and reliable to integrate Python logging with the Datadog Agent.

    This strategy example:
      - Creates a Python logger.
      - Outputs logs to stdout (the Datadog Agent reads stdout and forwards logs to Datadog).
      - Adds extra information (such as 'environment') to log messages.
    """

    def __init__(
        self,
        service: str,
        environment: str,
        project_id: str,
        repo_name: str,
        team: str,
        log_level: str = "INFO",
        logger_name: Optional[str] = None,
    ):
        """
        :param service: The service name (Datadog automatically recognizes this field as 'service').
        :param environment: The environment name (Datadog recognizes this as 'env').
        :param project_id: GCP project identifier (custom field).
        :param repo_name: Repository name (custom field).
        :param team: Team identifier (custom field).
        :param log_level: Logging level (default=INFO).
        :param logger_name: An optional logger name (defaults to 'datadog_logger_strategy').
        """
        self.service = service
        self.environment = environment
        self.project_id = project_id
        self.repo_name = repo_name
        self.team = team
        self.logger_name = logger_name or "datadog_logger_strategy"

        # Create or retrieve a logger

        self._logger = logging.getLogger(self.logger_name)
        self._logger.propagate = False  # stops logs from traveling to the root logger
        level_map = logging.getLevelNamesMapping()
        self._logger.setLevel(level_map[log_level.upper()])

        # If no handler is attached yet, attach our custom JSON handler
        if not self._logger.handlers:
            console_handler = logging.StreamHandler()
            # Use our JSON formatter
            console_handler.setFormatter(
                JsonDatadogFormatter(
                    service=self.service,
                    environment=self.environment,
                    project_id=self.project_id,
                    repo_name=self.repo_name,
                    team=self.team,
                )
            )
            self._logger.addHandler(console_handler)

            # Now pass that handler to basicConfig
            logging.basicConfig(
                level=logging.INFO,
                handlers=[console_handler],
                # You can omit 'format' here, because we're setting a custom Formatter for the handler
            )

    def info(self, msg: str, *args, **kwargs) -> None:
        self._logger.info(msg, *args, **kwargs)

    def warning(self, msg: str, *args, **kwargs) -> None:
        self._logger.warning(msg, *args, **kwargs)

    def error(self, msg: str, *args, **kwargs) -> None:
        self._logger.error(msg, *args, **kwargs)

    def debug(self, msg: str, *args, **kwargs) -> None:
        self._logger.debug(msg, *args, **kwargs)
