from ..error.errors import CsvSerializeError
from .serializer import Serializer


class CsvSerializer(Serializer):
    def serialize(self, data):
        if not data:
            raise CsvSerializeError("CSV serialization failed", "No data provided")
        csv_data = ",".join(data.values())
        return csv_data
