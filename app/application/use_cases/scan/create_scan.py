from app.domain.entities.scan import Scan
from app.domain.repositories.scan_repository import ScanRepository
from datetime import datetime
from uuid import UUID
import uuid


class CreateScanUseCase:
    def __init__(self, scan_repository: ScanRepository):
        self.scan_repository = scan_repository

    def execute(
        self,
        user_id: UUID,
        received_file_url: str,
        scanned_file_url: str,
        received_file_name: str,
        original_file_name: str,
        scanned_file_name: str,
    ) -> Scan:
        new_scan = Scan(
            id=uuid.uuid4(),
            user_id=user_id,
            received_file_url=received_file_url,
            scanned_file_url=scanned_file_url,
            received_file_name=received_file_name,
            original_file_name=original_file_name,
            scanned_file_name=scanned_file_name,
            created_at=datetime.now(),
        )

        try:
            return self.scan_repository.save(new_scan)
        finally:
            self.scan_repository.close()