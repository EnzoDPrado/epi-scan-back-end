from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session

from app.application.use_cases.epi.detect_epi import DetectEpiUseCase
from app.application.use_cases.file.upload_file_on_local import UploadFileOnLocalUseCase
from app.application.use_cases.epi.scan_epi import ScanEpiUseCase
from app.application.use_cases.scan.create_scan import CreateScanUseCase
from app.application.use_cases.storage.upload_file_on_storage import UploadFileOnStorageUseCase
from app.infrastructure.ai.yolo.yolo_service import YoloService
from app.infrastructure.persistence.repositories.scan_repository_pg import ScanRepositoryPg
from app.infrastructure.persistence.database import get_db
from fastapi.responses import Response

from app.infrastructure.dependencies.auth_dependency import auth_dependency
from app.infrastructure.storage.s3.s3_storage_service import S3StorageService


router = APIRouter(prefix="/epi", tags=["EPI"])

@router.post("")
async def scan_epi(
    file: UploadFile = File(...),
    user = Depends(auth_dependency),
    db_session: Session = Depends(get_db),
):
    upload_file_use_case = UploadFileOnLocalUseCase()

    object_detection_service = YoloService("runs/detect/train/weights/best.pt")
    detect_epi_use_case = DetectEpiUseCase(object_detection_service)

    storage_service = S3StorageService()

    upload_file_on_storage_use_case = UploadFileOnStorageUseCase(storage_service)
    scan_repository = ScanRepositoryPg(db_session)
    create_scan_use_case = CreateScanUseCase(scan_repository)

    scan_epi_use_case = ScanEpiUseCase(
        detect_epi_use_case,
        upload_file_use_case,
        upload_file_on_storage_use_case,
        create_scan_use_case,
    )

    detections, image_bytes = await scan_epi_use_case.execute(file, user_id=user["id"])

    return Response(
        content=image_bytes,
        media_type="image/jpeg"
    )