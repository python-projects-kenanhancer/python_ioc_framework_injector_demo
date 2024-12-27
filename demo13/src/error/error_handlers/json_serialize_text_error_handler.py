import logging

from ..errors import JsonSerializeError
from .error_handler import ErrorHandler


class JsonSerializeTextErrorHandler(ErrorHandler):
    def handle_error(self, error: JsonSerializeError):
        logging.error(
            f"JSON Serialization error occurred: {error}. Detail: {error.detail}."
        )
