from pydantic import BaseModel


class CdtToNexumSettings(BaseModel):
    airflow_home: str
    gcp_project: str
    google_application_credentials: str
    cdt_dataset: str
    google_cloud_project: str
    no_proxy: str
    dataset_output_env: str
    inttest_dset: str
