from greeting import AppConfig, GreetingType
from injector import Module, provider, singleton


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
