import uuid
from app.domain.entities.scan import Scan
from app.domain.exceptions.business_rule_exception import BusinessRuleException
from app.domain.repositories.scan_repository import ScanRepository


class FindScanByIdUseCase:
    def __init__(self, scan_repository: ScanRepository):
        self.scan_repository=scan_repository

    def execute(self, id: uuid.UUID) -> Scan:
        try:
            scan = self.scan_repository.findById(id)
        finally:
            self.scan_repository.close()

        if scan is None:
            raise BusinessRuleException("Escaneamento com este id não foi encontrado")

        return scan    