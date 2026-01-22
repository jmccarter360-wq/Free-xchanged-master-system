class CustomException(Exception):
    """Base class for custom exceptions."""
    pass


class NotFoundError(CustomException):
    """Exception raised for not found errors."""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class ValidationError(CustomException):
    """Exception raised for validation errors."""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def handle_exception(exc):
    """Function to handle exceptions and return a descriptive error message."""
    if isinstance(exc, NotFoundError):
        return {'error': 'Not Found', 'message': exc.message}, 404
    elif isinstance(exc, ValidationError):
        return {'error': 'Validation Error', 'message': exc.message}, 400
    else:
        return {'error': 'Internal Server Error', 'message': 'An unexpected error occurred.'}, 500
