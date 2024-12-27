import logging

from ..errors import CsvSerializeError
from .error_handler import ErrorHandler


class CsvSerializeTextErrorHandler(ErrorHandler):
    def handle_error(self, error: CsvSerializeError):
        logging.error(
            f"CSV Serialization error occurred: {error}. Detail: {error.detail}."
        )
