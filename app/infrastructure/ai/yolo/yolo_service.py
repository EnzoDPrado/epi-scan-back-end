from ultralytics import YOLO
import cv2

from app.domain.services.object_detection_service import ObjectDetectionService

class YoloService(ObjectDetectionService):
    def __init__(self, model_path: str = "yolov8n.pt"):
        self.model = YOLO(model_path)

    def detect(self, image_path: str) -> tuple[list, bytes, str]:
        results = self.model(image_path)

        output = []

        for r in results:
            for box in r.boxes:
                output.append({
                    "class_id": int(box.cls[0]),
                    "confidence": float(box.conf[0]),
                    "bbox": box.xyxy[0].tolist()
                })
        annotated_frame = r.plot()

        CONTENT_TYPE_MAP = {
            "jpg": "image/jpeg",
            "jpeg": "image/jpeg",
            "png": "image/png",
            "webp": "image/webp",
        }

        encode_format = ".jpg"
        content_type = CONTENT_TYPE_MAP.get(encode_format.lstrip("."), "application/octet-stream")
        _, buffer = cv2.imencode(encode_format, annotated_frame)

        image_bytes = buffer.tobytes()

        return output, image_bytes, content_type