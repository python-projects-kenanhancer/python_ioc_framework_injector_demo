import logging
from .error_handler import ErrorHandler
from ..errors import XmlSerializeError


class XmlSerializeTextErrorHandler(ErrorHandler):
    def handle_error(self, error: XmlSerializeError):
        logging.error(f"XML Serialization error occurred: {error}. Detail: {error.detail}. Element: {error.element}")
