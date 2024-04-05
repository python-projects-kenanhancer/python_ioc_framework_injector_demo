import json
import logging
from .error_handler import ErrorHandler
from ..errors import XmlSerializeError


class XmlSerializeJsonErrorHandler(ErrorHandler):
    def handle_error(self, error: XmlSerializeError):
        error_info = {
            "error_type": "XmlSerializationError",
            "message": str(error),
            "detail": error.detail,
            "element": error.element
        }
        logging.error(json.dumps(error_info))
