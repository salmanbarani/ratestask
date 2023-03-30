class SQLEXECUTIONERROR(Exception):
    def __init__(self, message, *args, **kwargs) -> None:
        super().__init__(message)
        self.message = message
