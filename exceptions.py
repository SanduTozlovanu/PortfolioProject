class NotFoundException(Exception):
    def __init__(self, msg: str):
        self.msg = msg


class BadRequestException(Exception):
    def __init__(self, msg: str):
        self.msg = msg


class UnauthorizedException(Exception):
    def __init__(self):
        self.msg = "Invalid Credentials"


class ForbiddenException(Exception):
    def __init__(self, msg: str):
        self.msg = msg

class ConflictException(Exception):
    def __init(self, msg: str):
        self.msg = msg
