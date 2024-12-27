import json
import logging

from ..errors import XmlSerializeError
from .error_handler import ErrorHandler


class XmlSerializeJsonErrorHandler(ErrorHandler):
    def handle_error(self, error: XmlSerializeError):
        error_info = {
            "error_type": "XmlSerializationError",
            "message": str(error),
            "detail": error.detail,
            "element": error.element,
        }
        logging.error(json.dumps(error_info))
