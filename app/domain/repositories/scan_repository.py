from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.scan import Scan

class ScanRepository(ABC):
    @abstractmethod
    def save(self, scan: Scan) -> Scan:
        pass


    @abstractmethod
    def findByUserId(self, id: UUID) -> Scan:
        pass