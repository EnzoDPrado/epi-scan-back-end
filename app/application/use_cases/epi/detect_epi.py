import os
from app.domain.services.object_detection_service import ObjectDetectionService
from app.domain.exceptions.business_rule_exception import BusinessRuleException

class DetectEpiUseCase() :
    def __init__(self, object_detection_service: ObjectDetectionService):
        self.object_detection_service = object_detection_service

    def execute(self, image_path: str) -> tuple[list, bytes]:
       try :
           detections, image_bytes, content_type = self.object_detection_service.detect(image_path)
           return detections, image_bytes, content_type
       except Exception as e:
           raise BusinessRuleException("Error detecting epi on image")
       finally:
           if os.path.exists(image_path):
               os.remove(image_path)   