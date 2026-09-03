class AppError(Exception):
    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class NotFoundError(AppError):
    def __init__(self, message="Recurso no encontrado"):
        super().__init__(message, status_code=404)


class ConflictError(AppError):
    def __init__(self, message="Conflicto con un recurso existente"):
        super().__init__(message, status_code=409)