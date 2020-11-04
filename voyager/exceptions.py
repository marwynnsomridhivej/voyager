class VoyagerException(ValueError):
    def __init__(self, message: str) -> None:
        super(VoyagerException, self).__init__(message)
        self.message = message


class MissingDependency(VoyagerException):
    def __init__(self, dependency: str) -> None:
        message = f"Dependency {dependency} is required to use this function"
        super(MissingDependency, self).__init__(message)


class HTTPException(VoyagerException):
    def __init__(self, code: int) -> None:
        message = f"HTTP Error Code: {code}"
        super(HTTPException, self).__init__(message)


class RateLimitException(VoyagerException):
    def __init__(self) -> None:
        super(RateLimitException, self).__init__(
            "You are being rate limited. Please try again later"
        )


class ResourceException(VoyagerException):
    def __init__(self, message: str) -> None:
        super(ResourceException, self).__init__(message)
