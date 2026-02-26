from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.application.dto.user.create_user_dto import CreateUserDTO
from app.application.dto.user.auth_user_dto import AuthUserDTO
from app.application.services.auth.auth_service import AuthService
from app.application.use_cases.user.auth_user import AuthUser
from app.application.use_cases.user.create_user import CreateUserUseCase
from app.application.use_cases.user.validate_exists_user_by_email import ValidateExistsUserByEmail
from app.infrastructure.persistence.repositories.user_repository_pg import UserRepositoryPg
from app.infrastructure.persistence.database import get_db

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("")
def create_user(dto: CreateUserDTO, db_session: Session = Depends(get_db)):

    userRepository = UserRepositoryPg(db_session)

    validate_exists_user_by_email = ValidateExistsUserByEmail(userRepository)
    create_user_use_case = CreateUserUseCase(userRepository, validate_exists_user_by_email)

    user_id = create_user_use_case.execute(dto.name, dto.email, dto.password)

    return {
        "id": user_id
    }

@router.post("/auth")
def auth_user(dto: AuthUserDTO, db_session: Session = Depends(get_db)):
    user_repository = UserRepositoryPg(db_session)
    auth_service = AuthService()
    auth_user_use_case = AuthUser(user_repository, auth_service)

    token = auth_user_use_case.execute(dto.email, dto.password)

    return {
        "token": token
    }