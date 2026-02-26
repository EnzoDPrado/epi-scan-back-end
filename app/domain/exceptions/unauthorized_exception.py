class UnauthorizedException(Exception):
     def __init__(self):
        self.message = "Bad credentials"
        super().__init__(self.message)