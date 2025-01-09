from pydantic import BaseModel


class AirflowInitSettings(BaseModel):
    db_upgrade: bool
    www_user_create: bool
    www_user_username: str
    www_user_password: str
