import json

from ..error.errors import JsonSerializeError
from .serializer import Serializer


class JsonSerializer(Serializer):
    def serialize(self, data):
        if not data:
            raise JsonSerializeError("JSON serialization failed", "No data provided")
        return json.dumps(data)
