import json
import logging
from ..errors import CsvSerializeError


def handle_csv_serialize_error_json(e: CsvSerializeError):
    error_info = {
        "error_type": "CsvSerializationError",
        "message": str(e),
        "detail": e.detail,
    }
    logging.error(json.dumps(error_info))
