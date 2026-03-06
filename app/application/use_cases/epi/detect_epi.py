import os
from app.application.services.yolo_service import YoloService
from app.domain.exceptions.business_rule_exception import BusinessRuleException


class DetectEpiUseCase() :
    def __init__(self, yolo_service: YoloService):
        self.yolo_service = yolo_service

    def execute(self, image_path: str) -> tuple[list, bytes]:
       try :
           detections, image_bytes, content_type = self.yolo_service.detect(image_path)
           return detections, image_bytes, content_type
       except Exception as e:
           print(e)
           raise BusinessRuleException("Error detecting epi on image")
       finally:
           if os.path.exists(image_path):
               os.remove(image_path)   