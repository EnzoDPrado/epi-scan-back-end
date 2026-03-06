import uuid

from app.application.use_cases.file.delete_file_on_storage import DeleteFileOnStorageUseCase
from app.application.use_cases.scan.find_scan_by_id import FindScanByIdUseCase
from app.domain.entities.scan import Scan
from app.domain.exceptions.business_rule_exception import BusinessRuleException
from app.domain.repositories.scan_repository import ScanRepository

class DeleteScanByIdUseCase():
    def __init__(self, 
            scan_repository: ScanRepository, 
            delete_file_on_storage_use_case: DeleteFileOnStorageUseCase,
            find_scan_by_id_use_case: FindScanByIdUseCase
        ):
        self.scan_repository = scan_repository
        self.delete_file_on_storage_use_case = delete_file_on_storage_use_case
        self.find_scan_by_id_use_case = find_scan_by_id_use_case

    def execute(self, id: uuid.UUID):
        scan = self.find_scan_by_id_use_case.execute(id)

        self.delete_file_on_storage_use_case.execute(scan.received_file_name)
        self.delete_file_on_storage_use_case.execute(scan.scanned_file_name)

        self._delete_scan(scan)


    def _delete_scan(self, scan: Scan):
        try:
            self.scan_repository.delete(scan)
        finally:
            self.scan_repository.close()
