from .serialize_error import SerializeError


class CsvSerializeError(SerializeError):
    def __init__(self, message="", detail=""):
        super().__init__(message, detail)
