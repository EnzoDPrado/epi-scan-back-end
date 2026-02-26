from app.domain.repositories.user_repository import UserRepository
from app.domain.entities.user import User
from sqlalchemy.orm import Session, undefer
from uuid import UUID

class UserRepositoryPg(UserRepository):
    def __init__(self, db_session: Session):
       self.db = db_session

    def save(self, user: User) -> User:
        try:
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)

            return user
        except Exception as e:
            self.db.rollback()
            raise e
        
    def findById(self, id: UUID) -> User:
        try:
            user = self.db.query(User).filter(
                User.id == id
            ).first()

            return user
        except Exception as e:
            self.db.rollback()
            raise e
        
    def findByEmail(self, email: str) -> User:
        try:
            user = self.db.query(User).filter(
                User.email == email,
                User.deleted_at.is_(None)
            ).options(
                undefer(User.password)
            ).first()

            return user
        except Exception as e:
            self.db.rollback()
            raise e

    def close(self):
        self.db.close()