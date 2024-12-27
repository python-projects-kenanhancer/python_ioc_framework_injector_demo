import logging

from ..errors import SerializeError
from .error_handler import ErrorHandler


class DefaultSerializeTextErrorHandler(ErrorHandler):
    def handle_error(self, error: SerializeError):
        logging.error(f"Serialization error occurred: {error}. Detail: {error.detail}.")
