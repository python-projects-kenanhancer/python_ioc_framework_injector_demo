from pydantic import BaseModel

from .greeting_language import GreetingLanguage
from .greeting_type import GreetingType


class SayHelloSettings(BaseModel):
    default_name: str
    greeting_type: GreetingType
    greeting_language: GreetingLanguage
