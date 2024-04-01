import json
from .serializer import Serializer
from ..error.errors import JsonSerializeError


class JsonSerializer(Serializer):
    def serialize(self, data):
        if not data:
            raise JsonSerializeError("JSON serialization failed", "No data provided")
        return json.dumps(data)
