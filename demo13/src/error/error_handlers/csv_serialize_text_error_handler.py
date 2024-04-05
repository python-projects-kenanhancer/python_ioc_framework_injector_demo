import logging
from .error_handler import ErrorHandler
from ..errors import CsvSerializeError


class CsvSerializeTextErrorHandler(ErrorHandler):
    def handle_error(self, error: CsvSerializeError):
        logging.error(f"CSV Serialization error occurred: {error}. Detail: {error.detail}.")
