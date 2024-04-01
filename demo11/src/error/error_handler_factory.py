import logging


class ErrorHandlerFactory:
    def __init__(self):
        self.error_handlers = {}

    def register_handler(self, error_type, handler_func):
        self.error_handlers[error_type] = handler_func

    def get_handler(self, error_type):
        return self.error_handlers.get(error_type, self.error_handlers.get(Exception))

    def handle_error(self, ex: Exception):
        handler_func = self.get_handler(type(ex))
        if handler_func:
            handler_func(ex)
        else:
            logging.error(f"No handler for error: {ex}")
