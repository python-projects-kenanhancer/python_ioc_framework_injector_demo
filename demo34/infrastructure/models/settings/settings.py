from pydantic import BaseModel

from . import (
    AirflowCoreSettings,
    AirflowInitSettings,
    BackendDBSettings,
    CdtToNexumSettings,
    DatadogSettings,
    Environment,
    FeatureFlagsSettings,
    MetaDatabaseSettings,
)


class Settings(BaseModel):
    project_env: Environment | None = None

    feature_flags: FeatureFlagsSettings | None = None
    meta_database: MetaDatabaseSettings | None = None
    backend_db: BackendDBSettings | None = None
    airflow_init: AirflowInitSettings | None = None
    airflow_core: AirflowCoreSettings | None = None
    cdt_to_nexum: CdtToNexumSettings | None = None
    datadog: DatadogSettings | None = None
