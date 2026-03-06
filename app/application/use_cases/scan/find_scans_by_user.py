from typing import List
from uuid import UUID

from app.domain.entities.scan import Scan
from app.domain.repositories.scan_repository import ScanRepository

class FindScansByUserUseCase:
    def __init__(self, scan_repository: ScanRepository):
        self.scan_repository = scan_repository

    def execute(self, user_id: UUID) -> List[Scan]:
        try:
            return self.scan_repository.find_by_user_id(user_id)
        finally:
            self.scan_repository.close()