from datetime import datetime
from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.application.use_cases.user.validate_exists_user_by_email import ValidateExistsUserByEmail
from app.domain.exceptions.business_rule_exception import BusinessRuleException

import bcrypt 
import uuid

class CreateUserUseCase:
    def __init__(
            self, 
            user_repository: UserRepository,
            validate_exists_user_by_email: ValidateExistsUserByEmail    
        ):
        self.user_repository = user_repository
        self.validate_exists_user_by_email_use_case = validate_exists_user_by_email

    def execute(self, name: str, email: str, password: str) -> uuid.UUID:
        
        self._validate_email(email)

        
        newUser = User(
            id= uuid.uuid4(),
            password= self._encrypt_password(password),
            created_at = datetime.now(),
            name = name,
            email = email,
        )

        try:
            self.user_repository.save(newUser)
        finally:
            self.user_repository.close()

        return newUser.id

    def _validate_email(self, email: str):
        exists_by_email = self.validate_exists_user_by_email_use_case.execute(email)

        if(exists_by_email):
            raise BusinessRuleException("Already exists a user with this email")

    def _encrypt_password(self, password: str):
        password_bytes = password.encode()
        hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
        return hashed.decode()
