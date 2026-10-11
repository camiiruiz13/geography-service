
class CountryStateCityException(Exception):

    def __init__(
        self,
        code: str,
        error: str,
        message: str,
        status_code: int = 502,
    ):
        super().__init__(message)
        self.code = code
        self.error = error
        self.message = message
        self.status_code = status_code
