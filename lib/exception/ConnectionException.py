class ConnectionException(BaseException):
    """raised when no connection could be established"""
    def __init__(self, message='Connection Failed'):
        self.message = message
        super().__init__(message)
