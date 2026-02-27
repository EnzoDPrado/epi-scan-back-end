from jose import jwt, JWTError
from app.domain.exceptions.unauthorized_exception import UnauthorizedException
from app.domain.entities.user import User
from datetime import datetime, time, timedelta
import os

class AuthService():
    def __init__(self):
        self.SECRET_KEY = os.getenv("SECRET_KEY")
        self.ALGORITH = os.getenv("ALGORITH")


    def generateJwt(self, user: User):
        userPayload = self._genPayload(user)
        token = jwt.encode(
            userPayload,
            self.SECRET_KEY,
            algorithm=self.ALGORITH
        )

        return token

    def decodeJWT(self, token: str):
        try:
            payload = jwt.decode(
                token,
                self.SECRET_KEY,
                algorithms=[self.ALGORITH]
            )
            return payload
        except JWTError:
            raise UnauthorizedException()

    def _genPayload(self, user: User):
        return {
            "id": str(user.id),
            "email": user.email,
            "deleted_at": user.deleted_at,
            "exp": self._generateExpirationTime(2)
        }

    def _generateExpirationTime(self, hours: int):
        return datetime.now() + timedelta(hours)