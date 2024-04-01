from injector import inject

from app_config import AppConfig


class DatabaseService:
    @inject
    def __init__(self, app_config: AppConfig):
        self.app_config = app_config

    def connect(self):
        print(f"Connecting to database at {self.app_config.database_url}")
