import json
import logging


def handle_general_error_json(e: Exception):
    error_info = {
        "error_type": "GeneralError",
        "message": str(e)
    }
    logging.error(json.dumps(error_info))
