import logging

from ..errors import DatabaseFetchError
from .error_handler import ErrorHandler


class DatabaseTextErrorHandler(ErrorHandler):
    def handle_error(self, error: DatabaseFetchError):
        logging.error(
            f"Database error occurred: {error}. Error code: {error.error_code}. Query: {error.query}"
        )
