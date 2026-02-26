from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.application.services.auth.auth_service import AuthService
from app.domain.exceptions.unauthorized_exception import UnauthorizedException

security = HTTPBearer()
auth_service = AuthService()

def auth_dependency(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    try:
        payload = auth_service.decodeJWT(token)
        return payload
    except Exception:
        raise UnauthorizedException()