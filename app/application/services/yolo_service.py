from ultralytics import YOLO
import os


class YoloService:

    def __init__(self, model_path: str = "yolov8n.pt"):
        self.model = YOLO(model_path)

    def detect(self, image_name: str):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
        image_path = os.path.join(base_dir, "uploads", image_name)

        results = self.model(image_path)

        output = []

        for r in results:
            for box in r.boxes:
                output.append({
                    "class_id": int(box.cls[0]),
                    "confidence": float(box.conf[0]),
                    "bbox": box.xyxy[0].tolist()
                })

        return output