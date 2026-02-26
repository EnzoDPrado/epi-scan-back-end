class BusinessRuleException(Exception):
     def __init__(self, message="Business rule exception"):
        self.message = message
        super().__init__(self.message)