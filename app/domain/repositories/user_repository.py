from abc import ABC, abstractmethod
from app.domain.entities.user import User
from uuid import UUID

class UserRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> User:
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> User:
        pass

    @abstractmethod
    def find_by_id(self, id: UUID) -> User:
        pass

    @abstractmethod
    def close(self):
        pass