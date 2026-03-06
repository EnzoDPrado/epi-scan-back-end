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

    @abstractmethod
    def findById(self, id: UUID) -> Scan:
        pass

    @abstractmethod
    def delete(self, scan: Scan):
        pass

    @abstractmethod
    def close(self):
        pass