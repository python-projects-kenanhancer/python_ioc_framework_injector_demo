import logging
from .error_handler import ErrorHandler
from ..errors import JsonSerializeError


class JsonSerializeTextErrorHandler(ErrorHandler):
    def handle_error(self, error: JsonSerializeError):
        logging.error(f"JSON Serialization error occurred: {error}. Detail: {error.detail}.")
