from fastapi import APIRouter, Depends, UploadFile, File
import shutil
from pathlib import Path

from app.infrastructure.dependencies.auth_dependency import auth_dependency


router = APIRouter(prefix="/epi", tags=["EPI"])

@router.post("")
async def scan_epi(
    file: UploadFile = File(...),
    user = Depends(auth_dependency)
):
    upload_dir = Path("uploads")
    upload_dir.mkdir(exist_ok=True)

    file_path = upload_dir / file.filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "message": "authorized",
        "filename": file.filename
    }