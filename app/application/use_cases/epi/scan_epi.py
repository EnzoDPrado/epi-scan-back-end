from fastapi import UploadFile, File
from app.application.use_cases.file.upload_file import UploadFileUseCase
from app.application.services.yolo_service import YoloService
from app.application.use_cases.storage.upload_file_on_storage import UploadFileOnStorageUseCase
from app.domain.exceptions.business_rule_exception import BusinessRuleException
import os

class ScanEpiUseCase :
    def __init__(
            self,
            upload_file_use_case: UploadFileUseCase,
            yolo_service: YoloService,
            upload_file_on_storage_use_case: UploadFileOnStorageUseCase
        ):
        self.upload_file_use_case = upload_file_use_case
        self.yolo_service = yolo_service
        self.upload_file_on_storage_use_case = upload_file_on_storage_use_case

    async def execute(self, file: UploadFile = File(...)):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
        upload_dir = f"{base_dir}/uploads"

        file_name = await self.upload_file_use_case.execute(upload_dir, file)
        image_path = f"{upload_dir}/{file_name}"

        detections, image_bytes = self._detect_epi(image_path)
        

    async def _upload_received_picture(self, upload_dir: str, file: UploadFile = File(...)) -> tuple[str, str]:
        file_name = await self.upload_file_use_case.execute(upload_dir, file)


    def _detect_epi(self, image_path: str) -> tuple[list, bytes]:
        try :
            detections, image_bytes = self.yolo_service.detect(image_path)
            return detections, image_bytes
        except Exception as e:
            raise BusinessRuleException("Error detecting epi on image")


    # def _


    #     # finally:
    #     #     if os.path.exists(image_path):
    #     #         os.remove(image_path)
        
