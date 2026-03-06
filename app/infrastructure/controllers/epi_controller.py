from fastapi import APIRouter, Depends, UploadFile, File
from app.application.use_cases.epi.detect_epi import DetectEpiUseCase
from app.application.use_cases.file.upload_file_on_local import UploadFileOnLocalUseCase
from app.application.use_cases.epi.scan_epi import ScanEpiUseCase
from app.application.services.yolo_service import YoloService
from fastapi.responses import Response

from app.infrastructure.dependencies.auth_dependency import auth_dependency
from app.infrastructure.services.s3_storage_service import S3StorageService


router = APIRouter(prefix="/epi", tags=["EPI"])

@router.post("")
async def scan_epi(
    file: UploadFile = File(...),
    user = Depends(auth_dependency)
):
    upload_file_use_case = UploadFileOnLocalUseCase()

    yolo_service = YoloService("runs/detect/train/weights/best.pt")
    detect_epi_use_case = DetectEpiUseCase(yolo_service)

    storage_service = S3StorageService()
    scan_epi_use_case = ScanEpiUseCase(
        detect_epi_use_case,
        upload_file_use_case,
        yolo_service,
        storage_service
    )

    detections, image_bytes = await scan_epi_use_case.execute(file)

    return Response(
        content=image_bytes,
        media_type="image/jpeg"
    )