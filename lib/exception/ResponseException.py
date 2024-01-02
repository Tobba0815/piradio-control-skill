class ResponseException(Exception):
    def __init__(self, message="No response or response is not valid", timeout=False):
        self.message = message
        self.timeout = timeout
        super().__init__(message)
