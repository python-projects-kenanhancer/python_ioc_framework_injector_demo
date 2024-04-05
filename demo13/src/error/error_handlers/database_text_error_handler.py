import logging
from .error_handler import ErrorHandler
from ..errors import DatabaseFetchError


class DatabaseTextErrorHandler(ErrorHandler):
    def handle_error(self, error: DatabaseFetchError):
        logging.error(f"Database error occurred: {error}. Error code: {error.error_code}. Query: {error.query}")
