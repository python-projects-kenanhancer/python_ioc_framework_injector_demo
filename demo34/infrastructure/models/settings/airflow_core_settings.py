from pydantic import BaseModel


class AirflowCoreSettings(BaseModel):
    fernet_key: str
    dags_are_paused_at_creation: bool
    load_examples: bool
    airflow_uid: int
