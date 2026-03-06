from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.application.use_cases.scan.find_scans_by_user import FindScansByUserUseCase
from app.infrastructure.persistence.repositories.scan_repository_pg import ScanRepositoryPg
from app.infrastructure.persistence.database import get_db
from app.infrastructure.dependencies.auth_dependency import auth_dependency

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