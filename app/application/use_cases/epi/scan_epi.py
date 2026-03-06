from fastapi import UploadFile, File
from app.application.use_cases.epi.detect_epi import DetectEpiUseCase
from app.application.use_cases.file.upload_file_on_local import UploadFileOnLocalUseCase
from app.domain.services.object_detection_service import ObjectDetectionService
from app.application.use_cases.storage.upload_file_on_storage import UploadFileOnStorageUseCase
import os

class ScanEpiUseCase :
    def __init__(
            self,
            detect_epi_use_case: DetectEpiUseCase,
            upload_file_use_case: UploadFileOnLocalUseCase,
            upload_file_on_storage_use_case: UploadFileOnStorageUseCase
        ):
        self.upload_file_use_case = upload_file_use_case
        self.upload_file_on_storage_use_case = upload_file_on_storage_use_case
        self.detect_epi_use_case = detect_epi_use_case

        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
        self.upload_dir = f"{base_dir}/uploads"

    async def execute(self, file: UploadFile = File(...)):
        received_file_contents = await self._read_file(file)
        received_file_name = self.upload_file_use_case.execute(self.upload_dir, received_file_contents, file)
        image_path = f"{self.upload_dir}/{received_file_name}"

        detections, scanned_file_contents, scanned_file_content_type = self.detect_epi_use_case.execute(image_path)

        received_file_url, scanned_file_url = self._upload_images_on_storage(
            scanned_file_contents,
            scanned_file_content_type,
            file.content_type,       
            received_file_contents,  
            received_file_name,      
        )

        return detections, scanned_file_contents
        
    def _upload_images_on_storage(self,
                                scanned_file_contents: bytes,
                                scanned_file_content_type: str,
                                received_file_content_type: str,
                                received_file_contents: bytes,
                                received_file_name: str
                                ) -> tuple[str, str]:
        
        received_file_url = self.upload_file_on_storage_use_case.upload(
            content_type=received_file_content_type,
            file_name=received_file_name,
            file_bytes=received_file_contents
        )

        scanned_file_url = self.upload_file_on_storage_use_case.upload(
            content_type=scanned_file_content_type,
            file_name=".jpg",
            file_bytes=scanned_file_contents
        )

        return received_file_url, scanned_file_url

    async def _read_file(self, file: UploadFile = File(...)) -> bytes:
        file_contents = await file.read()
        await file.seek(0)

        return file_contents
