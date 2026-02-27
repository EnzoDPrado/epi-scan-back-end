from ultralytics import YOLO
import os
import cv2

class YoloService:

    def __init__(self, model_path: str = "yolov8n.pt"):
        self.model = YOLO(model_path)

    def detect(self, image_path: str):
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

        _, buffer = cv2.imencode(".jpg", annotated_frame)
        image_bytes = buffer.tobytes()

        return output, image_bytes