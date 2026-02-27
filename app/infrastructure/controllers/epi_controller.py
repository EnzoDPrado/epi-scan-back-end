from fastapi import APIRouter, Depends, UploadFile, File
from app.application.use_cases.file.upload_file import UploadFileUseCase
from app.application.use_cases.epi.scan_epi import ScanEpiUseCase
from app.application.services.yolo_service import YoloService
from fastapi.responses import Response

from app.infrastructure.dependencies.auth_dependency import auth_dependency


router = APIRouter(prefix="/epi", tags=["EPI"])

@router.post("")
async def scan_epi(
    file: UploadFile = File(...),
    user = Depends(auth_dependency)
):
    upload_file_use_case = UploadFileUseCase()
    yolo_service = YoloService("runs/detect/train/weights/last.pt")
    scan_epi_use_case = ScanEpiUseCase(upload_file_use_case, yolo_service)

    detections, image_bytes = scan_epi_use_case.execute(file)

    return Response(
        content=image_bytes,
        media_type="image/jpeg"
    )