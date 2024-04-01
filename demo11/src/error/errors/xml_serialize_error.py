from .serialize_error import SerializeError


class XmlSerializeError(SerializeError):
    def __init__(self, message="", detail="", element=""):
        super().__init__(message, detail)
        self.element = element
