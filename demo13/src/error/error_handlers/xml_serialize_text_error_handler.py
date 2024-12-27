import logging

from ..errors import XmlSerializeError
from .error_handler import ErrorHandler


class XmlSerializeTextErrorHandler(ErrorHandler):
    def handle_error(self, error: XmlSerializeError):
        logging.error(
            f"XML Serialization error occurred: {error}. Detail: {error.detail}. Element: {error.element}"
        )
