from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.application.use_cases.file.delete_file_on_storage import DeleteFileOnStorageUseCase
from app.application.use_cases.scan.delete_scan_by_id import DeleteScanByIdUseCase
from app.application.use_cases.scan.find_scan_by_id import FindScanByIdUseCase
from app.application.use_cases.scan.find_scans_by_user import FindScansByUserUseCase
from app.infrastructure.persistence.repositories.scan_repository_pg import ScanRepositoryPg
from app.infrastructure.persistence.database import get_db
from app.infrastructure.dependencies.auth_dependency import auth_dependency
from app.infrastructure.storage.s3.s3_storage_service import S3StorageService

router = APIRouter(prefix="/scans", tags=["Scans"])


@router.get("/logged-user")
def list_scans_by_user(
    user=Depends(auth_dependency),
    db_session: Session = Depends(get_db),
):
    scan_repository = ScanRepositoryPg(db_session)
    list_scans_use_case = FindScansByUserUseCase(scan_repository)

    scans = list_scans_use_case.execute(user["id"])

    return [scan.to_dict() for scan in scans]


@router.delete("/{id}", status_code=204)
def delete_scan_by_id(
    id: UUID,
    user=Depends(auth_dependency),
    db_session: Session = Depends(get_db),
):
    scan_repository = ScanRepositoryPg(db_session)
    storage_service = S3StorageService()

    delete_file_on_storage_use_case = DeleteFileOnStorageUseCase(storage_service)
    find_scan_by_id_use_case = FindScanByIdUseCase(scan_repository)
    delete_scan_by_id = DeleteScanByIdUseCase(scan_repository,delete_file_on_storage_use_case, find_scan_by_id_use_case)

    delete_scan_by_id.execute(id)