from ultralytics import YOLO
import os


class YoloService:

    def __init__(self, model_name: str = "yolov8n.pt"):
        self.model = YOLO(model_name)

    def detect_image(self, image_path: str):
        results = self.model(image_path)

        detections = []

        for result in results:
            boxes = result.boxes
            for box in boxes:
                detections.append({
                    "class_id": int(box.cls[0]),
                    "confidence": float(box.conf[0]),
                    "bbox": box.xyxy[0].tolist()
                })

        return detections

    def train(self, data_yaml_path: str):
        self.model.train(
            data=data_yaml_path,
            epochs=50,
            imgsz=640
        )