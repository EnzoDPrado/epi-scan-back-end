from typing import List
from app.domain.entities.scan import Scan
from app.domain.repositories.scan_repository import ScanRepository
from app.domain.repositories.user_repository import UserRepository
from app.domain.entities.user import User
from sqlalchemy.orm import Session, undefer
from uuid import UUID

class ScanRepositoryPg(ScanRepository):
    def __init__(self, db_session: Session):
       self.db = db_session

    def save(self, scan: Scan) -> Scan:
        try:
            self.db.add(scan)
            self.db.commit()
            self.db.refresh(scan)

            return scan
        except Exception as e:
            self.db.rollback()
            raise e
        
    def find_by_user_id(self, id: UUID) -> List[Scan]:
        try:
            scans = self.db.query(Scan).filter(
                Scan.user_id == id
            )

            return scans
        except Exception as e:
            self.db.rollback()
            raise e

    def find_by_id(self, id: UUID) -> Scan:
        try:
            scan = self.db.query(Scan).filter(
                Scan.id == id
            ).first()

            return scan
        except Exception as e:
            self.db.rollback()
            raise e
        

    def delete(self, scan: Scan):
        try:
            self.db.query(Scan).filter(
                Scan.id == scan.id
            ).delete()
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e
        
    def close(self):
        self.db.close()