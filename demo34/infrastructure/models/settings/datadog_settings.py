from typing import Optional

from pydantic import BaseModel


class DatadogSettings(BaseModel):
    service: str
    environment: str = "dev"
    project_id: str
    repo_name: str
    team: str
    log_level: str = "INFO"
    logger_name: Optional[str] = None
