class EventServiceError(Exception):
    def __init__(self, message="", service_name="", endpoint=""):
        super().__init__(message)
        self.service_name = service_name
        self.endpoint = endpoint
