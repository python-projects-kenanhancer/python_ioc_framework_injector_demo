import logging

from .error_handler import ErrorHandler


class DefaultTextErrorHandler(ErrorHandler):
    def handle_error(self, error: Exception):
        logging.error(f"An unexpected error occurred: {error}")
