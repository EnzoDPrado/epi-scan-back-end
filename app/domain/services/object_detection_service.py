from abc import ABC, abstractmethod


class ObjectDetectionService(ABC):
    @abstractmethod
    def detect(self, image_path: str) -> tuple[list, bytes, str]:
        pass