from pydantic import BaseModel, ConfigDict

from ..greeting_type import GreetingType


class AppConfig(BaseModel):
    database_url: str
    enable_feature_x: bool
    enable_feature_y: bool
    greeting_strategy: GreetingType

    model_config = ConfigDict(from_attributes=True)

    def to_dict(self) -> dict:
        # The typed decorator will call this to serialize the response
        return self.model_dump()

    @classmethod
    def from_dict(cls, data: dict):
        # The typed decorator will call this to parse incoming JSON
        return cls.model_validate(data)
