import logging
from .error_handler import ErrorHandler
from ..errors import SerializeError


class DefaultSerializeTextErrorHandler(ErrorHandler):
    def handle_error(self, error: SerializeError):
        logging.error(f"Serialization error occurred: {error}. Detail: {error.detail}.")
