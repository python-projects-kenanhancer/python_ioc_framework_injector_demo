import logging

from .error_handlers import ErrorHandler


class ErrorHandlerFactory:
    def __init__(self):
        self.error_handlers = {}

    def register_handler(self, error_type: type[Exception], error_handler: ErrorHandler):
        self.error_handlers[error_type] = error_handler

    def get_handler(self, error_type) -> ErrorHandler:
        return self.error_handlers.get(error_type, self.error_handlers.get(Exception))

    def handle_error(self, ex: Exception):
        error_type = type(ex)
        error_handler = self.get_handler(error_type)
        if error_handler:
            error_handler.handle_error(ex)
        else:
            logging.error(f"No handler for {error_type}: {ex}")
