from pydantic import BaseModel


class BackendDBSettings(BaseModel):
    sql_alchemy_conn: str
    load_default_connections: bool
