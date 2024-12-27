from .error_handler_factory import ErrorHandlerFactory
from .error_handlers import DatabaseJsonErrorHandler, XmlSerializeJsonErrorHandler
from .errors import DatabaseFetchError, XmlSerializeError


def configure_error_handlers() -> ErrorHandlerFactory:
    error_handler_factory = ErrorHandlerFactory()

    error_handler_factory.register_handler(
        DatabaseFetchError, DatabaseJsonErrorHandler()
    )
    error_handler_factory.register_handler(
        XmlSerializeError, XmlSerializeJsonErrorHandler()
    )

    return error_handler_factory
