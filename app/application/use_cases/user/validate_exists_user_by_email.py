from app.domain.repositories.user_repository import UserRepository


class ValidateExistsUserByEmail():
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, email: str) -> bool :
    
        exists = False

        try:
            user = self.user_repository.findByEmail(email)

            exists = user is not None
        finally:
            self.user_repository.close()

        return exists
