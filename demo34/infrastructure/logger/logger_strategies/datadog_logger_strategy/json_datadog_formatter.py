import json
import logging
from typing import cast


class JsonDatadogFormatter(logging.Formatter):
    """
    A custom JSON formatter that includes fields relevant for Datadog logs.
    """

    def __init__(self, service: str, environment: str, project_id: str, repo_name: str, team: str):
        super().__init__()
        self.service = service
        self.environment = environment
        self.project_id = project_id
        self.repo_name = repo_name
        self.team = team

    def format(self, record: logging.LogRecord) -> str:
        # Build the base log dictionary
        log_dict = {
            "message": record.getMessage(),
            "level": record.levelname,
            "logger": record.name,
            "timestamp": self.formatTime(record, self.datefmt),
            "service": self.service,  # recognized by Datadog as 'service' (often auto-tagged)
            "env": self.environment,  # recognized by Datadog as 'env'
            "project_id": self.project_id,  # custom field
            "repo_name": self.repo_name,  # custom field
            "team": self.team,  # custom field
            # You could add 'host' or 'hostname' if you'd like Datadog to treat that as the host dimension
        }

        # Optionally, add extra fields if they're present in the record
        if record.args and isinstance(record.args, dict):
            safe_args = cast(dict[str, str], record.args)
            log_dict.update(safe_args)

        return json.dumps(log_dict)
