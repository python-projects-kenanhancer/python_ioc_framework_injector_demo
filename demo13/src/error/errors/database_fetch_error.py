class DatabaseFetchError(Exception):
    def __init__(self, message="", error_code=None, query=""):
        super().__init__(message)
        self.error_code = error_code
        self.query = query
