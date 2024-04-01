import json
import logging
from ..errors import DatabaseFetchError


def handle_database_error_json(e: DatabaseFetchError):
    error_info = {
        "error_type": "DatabaseError",
        "message": str(e),
        "error_code": e.error_code,
        "query": e.query
    }
    logging.error(json.dumps(error_info))
