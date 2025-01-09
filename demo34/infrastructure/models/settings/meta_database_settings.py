from pydantic import BaseModel


class MetaDatabaseSettings(BaseModel):
    postgres_user: str
    postgres_password: str
    postgres_db: str
