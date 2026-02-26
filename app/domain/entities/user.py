from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import deferred
from sqlalchemy.dialects.postgresql import UUID
from app.infrastructure.persistence.database import Base
from datetime import datetime
import uuid


class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=False, nullable=False)
    password = deferred(Column(String(255), nullable=False))
    created_at = Column(DateTime, default=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)
    
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "email": self.email,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }