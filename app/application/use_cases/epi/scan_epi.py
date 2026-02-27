from fastapi import UploadFile, File
from app.application.use_cases.file.upload_file import UploadFileUseCase
from app.application.services.yolo_service import YoloService
from app.domain.exceptions.business_rule_exception import BusinessRuleException
import os

class ScanEpiUseCase :
    def __init__(
            self,
            upload_file_use_case: UploadFileUseCase,
            yolo_service: YoloService
        ):
        self.upload_file_use_case = upload_file_use_case
        self.yolo_service = yolo_service

    def execute(self, file: UploadFile = File(...)):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
        upload_dir = f"{base_dir}/uploads"

        file_name = self.upload_file_use_case.execute(upload_dir, file)
        image_path = f"{upload_dir}/{file_name}"

        try :
            detections, image_bytes = self.yolo_service.detect(image_path)
            return detections, image_bytes
        except Exception as e:
            raise BusinessRuleException("Error detecting epi on image")
        finally:
            if os.path.exists(image_path):
                os.remove(image_path)
        
