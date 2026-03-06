from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.infrastructure.persistence.database import base
from datetime import datetime
import uuid


class Scan(base):
    __tablename__ = "scans"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    received_file_url = Column(String, nullable=False)
    scanned_file_url = Column(String, nullable=False)
    received_file_name = Column(String, nullable=False)
    original_file_name = Column(String, nullable=False)
    scanned_file_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="scans") 

    def to_dict(self):
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "received_file_url": self.received_file_url,
            "scanned_file_url": self.scanned_file_url,
            "received_file_name": self.received_file_name,
            "original_file_name": self.original_file_name,
            "scanned_file_name": self.scanned_file_name,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }