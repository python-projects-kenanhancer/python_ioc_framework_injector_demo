class SerializeError(Exception):
    def __init__(self, message="", detail=""):
        super().__init__(message)
        self.detail = detail
