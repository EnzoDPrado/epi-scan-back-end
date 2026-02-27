from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.application.services.auth_service import AuthService
from app.domain.exceptions.unauthorized_exception import UnauthorizedException
import bcrypt

class AuthUser():
    def __init__(self, user_repository: UserRepository, auth_service: AuthService):
        self.user_repository = user_repository
        self.auth_service = auth_service

    def execute(self, email: str, password: str) :
        user = self._findUserByEmail(email)

        self._validate_password(password, user.password.encode())

        return self.auth_service.generateJwt(user)


    def _validate_password(self, passed_password: str, user_password: bytes):
        encrypted_passed_password = passed_password.encode()

        is_password_correctly = bcrypt.checkpw(encrypted_passed_password, user_password)

        if not is_password_correctly:
            raise UnauthorizedException()
        
    
    def _findUserByEmail(self, email: str) -> User:
        user = self.user_repository.findByEmail(email)

        if (user == None):
            raise UnauthorizedException()
        
        return user
